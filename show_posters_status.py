from django.core.management.base import BaseCommand
from films.models import Film
import os


class Command(BaseCommand):
    help = 'Показать статус всех постеров фильмов'

    def handle(self, *args, **options):
        self.stdout.write("🖼️ СТАТУС ПОСТЕРОВ ФИЛЬМОВ")
        self.stdout.write("=" * 60)
        
        films = Film.objects.all().order_by('id')
        
        original_count = 0
        generated_count = 0
        missing_count = 0
        
        self.stdout.write(f"\n📋 СПИСОК ВСЕХ ФИЛЬМОВ:")
        self.stdout.write("-" * 60)
        
        for film in films:
            if film.poster:
                poster_path = film.poster.name
                poster_type = "🎨 Сгенерированный"
                
                # Определяем тип постера по имени файла
                if any(word in poster_path.lower() for word in ['_poster.jpg', 'poster.jpg']):
                    if any(rus_char in poster_path for rus_char in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'):
                        poster_type = "🖼️ Оригинальный"
                        original_count += 1
                    else:
                        poster_type = "🎨 Стильный"
                        generated_count += 1
                elif 'scream_' in poster_path.lower():
                    poster_type = "🔪 Крик-стиль"
                    generated_count += 1
                else:
                    generated_count += 1
                
                # Проверяем существование файла
                file_exists = "✅" if os.path.exists(f"media/{poster_path}") else "❌"
                
                self.stdout.write(f"{film.id:2d}. {film.title:<20} ({film.year}) {poster_type} {file_exists}")
                self.stdout.write(f"    📁 {poster_path}")
            else:
                self.stdout.write(f"{film.id:2d}. {film.title:<20} ({film.year}) ❌ НЕТ ПОСТЕРА")
                missing_count += 1
            
            self.stdout.write("")
        
        total_films = films.count()
        
        self.stdout.write("=" * 60)
        self.stdout.write(f"📊 СТАТИСТИКА ПОСТЕРОВ:")
        self.stdout.write(f"  📁 Всего фильмов: {total_films}")
        self.stdout.write(f"  🖼️ Оригинальные постеры: {original_count}")
        self.stdout.write(f"  🎨 Стильные/сгенерированные: {generated_count}")
        self.stdout.write(f"  ❌ Без постеров: {missing_count}")
        self.stdout.write(f"  📊 Покрытие: {((total_films - missing_count)/total_films*100):.1f}%")
        
        self.stdout.write(f"\n🎯 ТИПЫ ПОСТЕРОВ:")
        self.stdout.write(f"  🖼️ Оригинальные - загружены с IMDB/Amazon")
        self.stdout.write(f"  🔪 Крик-стиль - созданы в стиле ужасов")
        self.stdout.write(f"  🎨 Стильные - сгенерированы с градиентами")
        
        if missing_count == 0:
            self.stdout.write(self.style.SUCCESS(f"\n🎉 ВСЕ ФИЛЬМЫ ИМЕЮТ ПОСТЕРЫ!"))
            self.stdout.write("🌟 TochkaFilms выглядит профессионально")
        else:
            self.stdout.write(self.style.WARNING(f"\n⚠️ Нужно добавить постеры для {missing_count} фильмов"))
        
        self.stdout.write(f"\n🌐 ТЕСТИРОВАНИЕ:")
        self.stdout.write(f"  1. Откройте http://127.0.0.1:8000/")
        self.stdout.write(f"  2. Проверьте главную страницу")
        self.stdout.write(f"  3. Посмотрите на карточки фильмов")
        self.stdout.write(f"  4. Убедитесь что все постеры загружаются")
        self.stdout.write(f"  5. Проверьте страницы отдельных фильмов")
        
        self.stdout.write(self.style.SUCCESS(f"\n🎬 TOCHKAFILMS - КРАСИВЫЕ ПОСТЕРЫ!"))