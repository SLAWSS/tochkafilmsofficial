from django.core.management.base import BaseCommand
from films.models import Film
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Показывает все постеры и их ссылки'

    def add_arguments(self, parser):
        parser.add_argument('--export', action='store_true', help='Экспортировать в файл')
        parser.add_argument('--check-files', action='store_true', help='Проверить существование файлов')

    def handle(self, *args, **options):
        if options['export']:
            self.export_posters_list()
        elif options['check_files']:
            self.check_poster_files()
        else:
            self.show_all_posters()

    def show_all_posters(self):
        """Показывает все постеры"""
        films = Film.objects.all().order_by('title')
        
        self.stdout.write("=" * 80)
        self.stdout.write("🖼️  СПИСОК ВСЕХ ПОСТЕРОВ")
        self.stdout.write("=" * 80)
        
        self.stdout.write(f"\n📊 СТАТИСТИКА:")
        self.stdout.write(f"  Всего фильмов: {films.count()}")
        
        films_with_posters = films.exclude(poster='')
        films_without_posters = films.filter(poster='')
        
        self.stdout.write(f"  С постерами: {films_with_posters.count()}")
        self.stdout.write(f"  Без постеров: {films_without_posters.count()}")
        
        self.stdout.write(f"\n📋 СПИСОК ПОСТЕРОВ:")
        self.stdout.write("-" * 80)
        
        for film in films_with_posters:
            poster_path = film.poster.name if film.poster else "НЕТ ПОСТЕРА"
            full_url = f"/media/{poster_path}" if film.poster else "НЕТ"
            file_path = os.path.join(settings.MEDIA_ROOT, poster_path) if film.poster else "НЕТ"
            
            # Проверяем существование файла
            file_exists = "✅" if film.poster and os.path.exists(file_path) else "❌"
            
            self.stdout.write(f"{file_exists} {film.title} ({film.year})")
            self.stdout.write(f"    БД путь: {poster_path}")
            self.stdout.write(f"    URL: {full_url}")
            self.stdout.write(f"    Файл: {file_path}")
            self.stdout.write("")
        
        if films_without_posters:
            self.stdout.write(f"\n⚠️  ФИЛЬМЫ БЕЗ ПОСТЕРОВ:")
            for film in films_without_posters:
                self.stdout.write(f"  • {film.title} ({film.year})")

    def check_poster_files(self):
        """Проверяет существование файлов постеров"""
        films = Film.objects.exclude(poster='')
        
        self.stdout.write("🔍 ПРОВЕРКА ФАЙЛОВ ПОСТЕРОВ")
        self.stdout.write("=" * 50)
        
        missing_files = []
        existing_files = []
        
        for film in films:
            if film.poster:
                file_path = os.path.join(settings.MEDIA_ROOT, film.poster.name)
                if os.path.exists(file_path):
                    existing_files.append(film)
                    self.stdout.write(f"✅ {film.title} - {film.poster.name}")
                else:
                    missing_files.append(film)
                    self.stdout.write(f"❌ {film.title} - ФАЙЛ НЕ НАЙДЕН: {film.poster.name}")
        
        self.stdout.write(f"\n📊 РЕЗУЛЬТАТ ПРОВЕРКИ:")
        self.stdout.write(f"  Файлы найдены: {len(existing_files)}")
        self.stdout.write(f"  Файлы отсутствуют: {len(missing_files)}")
        
        if missing_files:
            self.stdout.write(f"\n⚠️  ОТСУТСТВУЮЩИЕ ФАЙЛЫ:")
            for film in missing_files:
                self.stdout.write(f"  • {film.title}: {film.poster.name}")

    def export_posters_list(self):
        """Экспортирует список постеров в файл"""
        films = Film.objects.exclude(poster='').order_by('title')
        
        export_data = []
        export_data.append("# СПИСОК ВСЕХ ПОСТЕРОВ")
        export_data.append("=" * 50)
        export_data.append("")
        export_data.append(f"Всего фильмов с постерами: {films.count()}")
        export_data.append(f"Дата экспорта: {self.get_current_date()}")
        export_data.append("")
        
        # Группируем по типам постеров
        poster_types = {
            'family': [],
            'original': [],
            'poster': [],
            'other': []
        }
        
        for film in films:
            poster_name = film.poster.name.lower()
            if 'family_poster' in poster_name:
                poster_types['family'].append(film)
            elif 'original' in poster_name:
                poster_types['original'].append(film)
            elif 'poster' in poster_name:
                poster_types['poster'].append(film)
            else:
                poster_types['other'].append(film)
        
        # Экспортируем по группам
        for type_name, type_films in poster_types.items():
            if type_films:
                export_data.append(f"## {type_name.upper()} ПОСТЕРЫ ({len(type_films)})")
                export_data.append("")
                
                for film in type_films:
                    export_data.append(f"**{film.title}** ({film.year})")
                    export_data.append(f"- Файл: `{film.poster.name}`")
                    export_data.append(f"- URL: `/media/{film.poster.name}`")
                    export_data.append(f"- Рейтинг: ⭐ {film.rating}")
                    export_data.append("")
        
        # Сохраняем в файл
        filename = "POSTERS_LIST.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(export_data))
        
        self.stdout.write(f"✅ Список постеров экспортирован в файл: {filename}")

    def get_current_date(self):
        """Возвращает текущую дату"""
        from datetime import datetime
        return datetime.now().strftime("%d.%m.%Y %H:%M")

    def show_poster_statistics(self):
        """Показывает статистику по типам постеров"""
        films = Film.objects.exclude(poster='')
        
        stats = {
            'family_poster': 0,
            'original': 0,
            'poster': 0,
            'default_poster': 0,
            'other': 0
        }
        
        for film in films:
            poster_name = film.poster.name.lower()
            if 'family_poster' in poster_name:
                stats['family_poster'] += 1
            elif 'original' in poster_name:
                stats['original'] += 1
            elif 'default_poster' in poster_name:
                stats['default_poster'] += 1
            elif 'poster' in poster_name:
                stats['poster'] += 1
            else:
                stats['other'] += 1
        
        self.stdout.write(f"\n📊 СТАТИСТИКА ПО ТИПАМ ПОСТЕРОВ:")
        self.stdout.write(f"  🎭 Семейные постеры: {stats['family_poster']}")
        self.stdout.write(f"  🎬 Оригинальные: {stats['original']}")
        self.stdout.write(f"  📽️  Обычные постеры: {stats['poster']}")
        self.stdout.write(f"  🎨 Дефолтные: {stats['default_poster']}")
        self.stdout.write(f"  ❓ Другие: {stats['other']}")
        
        return stats