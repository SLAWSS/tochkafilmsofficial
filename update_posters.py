from django.core.management.base import BaseCommand
from films.models import Film
from django.core.files import File
from django.conf import settings
import os
import shutil


class Command(BaseCommand):
    help = 'Обновляет постеры фильмов'

    def add_arguments(self, parser):
        parser.add_argument('--film-id', type=int, help='ID фильма')
        parser.add_argument('--film-title', type=str, help='Название фильма')
        parser.add_argument('--poster-path', type=str, help='Путь к новому постеру')
        parser.add_argument('--list-films', action='store_true', help='Показать список фильмов')
        parser.add_argument('--backup', action='store_true', help='Создать резервную копию старого постера')

    def handle(self, *args, **options):
        if options['list_films']:
            self.list_films()
        elif options['film_id'] and options['poster_path']:
            self.update_poster_by_id(options['film_id'], options['poster_path'], options['backup'])
        elif options['film_title'] and options['poster_path']:
            self.update_poster_by_title(options['film_title'], options['poster_path'], options['backup'])
        else:
            self.show_help()

    def show_help(self):
        """Показывает справку по использованию"""
        self.stdout.write("🖼️  ОБНОВЛЕНИЕ ПОСТЕРОВ")
        self.stdout.write("=" * 40)
        self.stdout.write("")
        self.stdout.write("Использование:")
        self.stdout.write("  --list-films                    Показать все фильмы")
        self.stdout.write("  --film-id 123 --poster-path ... Обновить по ID")
        self.stdout.write("  --film-title 'Название' --poster-path ... Обновить по названию")
        self.stdout.write("  --backup                        Создать резервную копию")
        self.stdout.write("")
        self.stdout.write("Примеры:")
        self.stdout.write("  python manage.py update_posters --list-films")
        self.stdout.write("  python manage.py update_posters --film-id 1 --poster-path /path/to/new_poster.jpg")
        self.stdout.write("  python manage.py update_posters --film-title 'Начало' --poster-path poster.jpg --backup")

    def list_films(self):
        """Показывает список всех фильмов"""
        films = Film.objects.all().order_by('title')
        
        self.stdout.write("📋 СПИСОК ФИЛЬМОВ:")
        self.stdout.write("-" * 60)
        
        for film in films:
            poster_status = "✅" if film.poster else "❌"
            poster_name = film.poster.name if film.poster else "НЕТ ПОСТЕРА"
            
            self.stdout.write(f"{poster_status} ID {film.id:3d}: {film.title} ({film.year})")
            self.stdout.write(f"     Постер: {poster_name}")
            self.stdout.write("")

    def update_poster_by_id(self, film_id, poster_path, backup=False):
        """Обновляет постер по ID фильма"""
        try:
            film = Film.objects.get(id=film_id)
            self.update_film_poster(film, poster_path, backup)
        except Film.DoesNotExist:
            self.stdout.write(f"❌ Фильм с ID {film_id} не найден")

    def update_poster_by_title(self, film_title, poster_path, backup=False):
        """Обновляет постер по названию фильма"""
        try:
            film = Film.objects.get(title__icontains=film_title)
            self.update_film_poster(film, poster_path, backup)
        except Film.DoesNotExist:
            self.stdout.write(f"❌ Фильм '{film_title}' не найден")
        except Film.MultipleObjectsReturned:
            films = Film.objects.filter(title__icontains=film_title)
            self.stdout.write(f"❌ Найдено несколько фильмов с названием '{film_title}':")
            for film in films:
                self.stdout.write(f"  ID {film.id}: {film.title} ({film.year})")
            self.stdout.write("Используйте --film-id для точного выбора")

    def update_film_poster(self, film, poster_path, backup=False):
        """Обновляет постер конкретного фильма"""
        # Проверяем существование нового файла
        if not os.path.exists(poster_path):
            self.stdout.write(f"❌ Файл {poster_path} не найден")
            return

        self.stdout.write(f"🎬 Обновляю постер для: {film.title} ({film.year})")
        
        # Создаем резервную копию если нужно
        if backup and film.poster:
            self.create_backup(film)
        
        # Получаем старый путь
        old_poster_path = None
        if film.poster:
            old_poster_path = os.path.join(settings.MEDIA_ROOT, film.poster.name)
            self.stdout.write(f"📁 Старый постер: {film.poster.name}")
        
        try:
            # Открываем новый файл
            with open(poster_path, 'rb') as f:
                # Генерируем имя файла
                filename = self.generate_filename(film, poster_path)
                
                # Сохраняем новый постер
                film.poster.save(filename, File(f))
                
            self.stdout.write(f"✅ Новый постер: {film.poster.name}")
            
            # Удаляем старый файл если он существует и отличается от нового
            if old_poster_path and os.path.exists(old_poster_path):
                new_poster_path = os.path.join(settings.MEDIA_ROOT, film.poster.name)
                if old_poster_path != new_poster_path:
                    os.remove(old_poster_path)
                    self.stdout.write(f"🗑️  Удален старый файл: {os.path.basename(old_poster_path)}")
            
            self.stdout.write(f"✅ Постер успешно обновлен!")
            
        except Exception as e:
            self.stdout.write(f"❌ Ошибка обновления постера: {e}")

    def create_backup(self, film):
        """Создает резервную копию старого постера"""
        if not film.poster:
            return
        
        old_path = os.path.join(settings.MEDIA_ROOT, film.poster.name)
        if not os.path.exists(old_path):
            return
        
        # Создаем папку для резервных копий
        backup_dir = os.path.join(settings.MEDIA_ROOT, 'posters', 'backup')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Генерируем имя для резервной копии
        filename = os.path.basename(old_path)
        name, ext = os.path.splitext(filename)
        backup_filename = f"{name}_backup_{self.get_timestamp()}{ext}"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Копируем файл
        shutil.copy2(old_path, backup_path)
        self.stdout.write(f"💾 Создана резервная копия: backup/{backup_filename}")

    def generate_filename(self, film, poster_path):
        """Генерирует имя файла для постера"""
        ext = os.path.splitext(poster_path)[1]
        safe_title = film.title.lower().replace(' ', '_').replace(':', '').replace('(', '').replace(')', '')
        return f"{safe_title}_updated_poster{ext}"

    def get_timestamp(self):
        """Возвращает временную метку"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def batch_update_posters(self, posters_dir):
        """Массовое обновление постеров из папки"""
        if not os.path.exists(posters_dir):
            self.stdout.write(f"❌ Папка {posters_dir} не найдена")
            return
        
        self.stdout.write(f"📁 Массовое обновление из папки: {posters_dir}")
        
        # Получаем все файлы изображений
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
        poster_files = []
        
        for filename in os.listdir(posters_dir):
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                poster_files.append(filename)
        
        self.stdout.write(f"Найдено {len(poster_files)} файлов изображений")
        
        updated_count = 0
        for filename in poster_files:
            # Пытаемся найти фильм по имени файла
            film_title = self.extract_title_from_filename(filename)
            if film_title:
                try:
                    film = Film.objects.get(title__icontains=film_title)
                    poster_path = os.path.join(posters_dir, filename)
                    self.update_film_poster(film, poster_path)
                    updated_count += 1
                except Film.DoesNotExist:
                    self.stdout.write(f"⚠️  Фильм не найден для файла: {filename}")
                except Film.MultipleObjectsReturned:
                    self.stdout.write(f"⚠️  Несколько фильмов найдено для: {filename}")
        
        self.stdout.write(f"✅ Обновлено постеров: {updated_count}")

    def extract_title_from_filename(self, filename):
        """Извлекает название фильма из имени файла"""
        # Убираем расширение
        name = os.path.splitext(filename)[0]
        
        # Убираем общие суффиксы
        suffixes = ['_poster', '_original', '_family_poster', '_default_poster']
        for suffix in suffixes:
            if name.endswith(suffix):
                name = name[:-len(suffix)]
                break
        
        # Заменяем подчеркивания на пробелы
        title = name.replace('_', ' ').title()
        
        return title if len(title) > 2 else None