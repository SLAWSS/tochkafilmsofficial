from django.core.management.base import BaseCommand
from films.models import Film
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import os
import time


class Command(BaseCommand):
    help = 'Скачивает и добавляет постеры для фильмов'

    def add_arguments(self, parser):
        parser.add_argument('--film-id', type=int, help='ID конкретного фильма')
        parser.add_argument('--all-missing', action='store_true', help='Добавить постеры всем фильмам без них')

    def handle(self, *args, **options):
        if options['film_id']:
            try:
                film = Film.objects.get(id=options['film_id'])
                self.add_poster_to_film(film)
            except Film.DoesNotExist:
                self.stdout.write(f"Фильм с ID {options['film_id']} не найден")
        elif options['all_missing']:
            self.add_posters_to_missing_films()
        else:
            self.stdout.write("Используйте --film-id или --all-missing")

    def get_poster_urls(self):
        """Возвращает словарь с URL постеров"""
        return {
            "Тестовый фильм": "https://image.tmdb.org/t/p/w500/6KErczPBROQty7QoIsaa6wJYXZi.jpg",
            "Начало": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
            "Интерстеллар": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
            "Темный рыцарь": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
            "Матрица": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
            "Форрест Гамп": "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
            "Побег из Шоушенка": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
            "Криминальное чтиво": "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
            "Бойцовский клуб": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
            "Джокер": "https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg",
            "Мстители: Финал": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
            "Дюна": "https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg",
            "Паразиты": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
        }

    def download_poster(self, url):
        """Скачивает постер по URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                return response.content
            else:
                self.stdout.write(f"Ошибка загрузки: {response.status_code}")
                return None
        except Exception as e:
            self.stdout.write(f"Ошибка: {e}")
            return None

    def add_poster_to_film(self, film):
        """Добавляет постер к фильму"""
        poster_urls = self.get_poster_urls()
        
        if film.title not in poster_urls:
            self.stdout.write(f"⚠️  Нет URL постера для '{film.title}'")
            return False

        try:
            self.stdout.write(f"Загружаю постер для '{film.title}'...")
            
            poster_data = self.download_poster(poster_urls[film.title])
            if not poster_data:
                return False
            
            # Создаем временный файл
            temp_file = NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_file.write(poster_data)
            temp_file.close()
            
            # Сохраняем в модель
            filename = f"{film.title.lower().replace(' ', '_').replace(':', '')}_poster.jpg"
            with open(temp_file.name, 'rb') as f:
                film.poster.save(filename, File(f))
            
            # Удаляем временный файл
            os.unlink(temp_file.name)
            
            self.stdout.write(f"✅ Постер добавлен для '{film.title}'")
            return True
            
        except Exception as e:
            self.stdout.write(f"❌ Ошибка добавления постера для '{film.title}': {e}")
            return False

    def add_posters_to_missing_films(self):
        """Добавляет постеры всем фильмам без них"""
        films = Film.objects.all()
        missing_films = []
        
        # Находим фильмы без постеров
        for film in films:
            if not film.poster:
                missing_films.append(film)
        
        if not missing_films:
            self.stdout.write("Все фильмы уже имеют постеры!")
            return
        
        self.stdout.write(f"Найдено {len(missing_films)} фильмов без постеров")
        
        success_count = 0
        for film in missing_films:
            if self.add_poster_to_film(film):
                success_count += 1
            time.sleep(1)  # Пауза между запросами
        
        self.stdout.write(f"\nДобавлено постеров: {success_count} из {len(missing_films)}")