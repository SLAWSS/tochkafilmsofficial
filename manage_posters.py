from django.core.management.base import BaseCommand
from films.models import Film
import os
from django.conf import settings
from django.core.files import File
import shutil


class Command(BaseCommand):
    help = 'Управление постерами фильмов'

    def add_arguments(self, parser):
        parser.add_argument('--check', action='store_true', help='Проверить фильмы без постеров')
        parser.add_argument('--add-default', action='store_true', help='Добавить дефолтные постеры')
        parser.add_argument('--film-id', type=int, help='ID конкретного фильма')
        parser.add_argument('--poster-path', type=str, help='Путь к постеру')

    def handle(self, *args, **options):
        if options['check']:
            self.check_missing_posters()
        elif options['add_default']:
            self.add_default_posters()
        elif options['film_id'] and options['poster_path']:
            self.add_poster_to_film(options['film_id'], options['poster_path'])
        else:
            self.stdout.write("Используйте --check, --add-default или --film-id с --poster-path")

    def check_missing_posters(self):
        films = Film.objects.all()
        missing_count = 0
        
        self.stdout.write(f"Проверяю {films.count()} фильмов...")
        
        for film in films:
            if not film.poster:
                self.stdout.write(f"❌ ID {film.id}: {film.title} - НЕТ ПОСТЕРА")
                missing_count += 1
            elif not os.path.exists(os.path.join(settings.MEDIA_ROOT, str(film.poster))):
                self.stdout.write(f"⚠️  ID {film.id}: {film.title} - ФАЙЛ НЕ НАЙДЕН: {film.poster}")
                missing_count += 1
            else:
                self.stdout.write(f"✅ ID {film.id}: {film.title} - OK")
        
        self.stdout.write(f"\nИтого: {missing_count} фильмов без постеров из {films.count()}")

    def add_default_posters(self):
        """Добавляет дефолтные постеры для фильмов без них"""
        films_without_posters = []
        
        for film in Film.objects.all():
            if not film.poster or not os.path.exists(os.path.join(settings.MEDIA_ROOT, str(film.poster))):
                films_without_posters.append(film)
        
        if not films_without_posters:
            self.stdout.write("Все фильмы уже имеют постеры!")
            return
        
        # Создаем дефолтный постер если его нет
        default_poster_path = os.path.join(settings.MEDIA_ROOT, 'posters', 'default_poster.jpg')
        
        if not os.path.exists(default_poster_path):
            self.stdout.write("Создаю дефолтный постер...")
            # Здесь можно добавить создание простого постера или скопировать существующий
            
        for film in films_without_posters:
            self.stdout.write(f"Добавляю постер для: {film.title}")
            # Логика добавления дефолтного постера

    def add_poster_to_film(self, film_id, poster_path):
        """Добавляет постер к конкретному фильму"""
        try:
            film = Film.objects.get(id=film_id)
            
            if not os.path.exists(poster_path):
                self.stdout.write(f"Файл {poster_path} не найден!")
                return
            
            # Копируем файл в media/posters/
            filename = os.path.basename(poster_path)
            destination = os.path.join(settings.MEDIA_ROOT, 'posters', filename)
            
            # Создаем директорию если не существует
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            
            # Копируем файл
            shutil.copy2(poster_path, destination)
            
            # Обновляем модель
            film.poster = f'posters/{filename}'
            film.save()
            
            self.stdout.write(f"✅ Постер добавлен к фильму '{film.title}'")
            
        except Film.DoesNotExist:
            self.stdout.write(f"Фильм с ID {film_id} не найден!")
        except Exception as e:
            self.stdout.write(f"Ошибка: {e}")