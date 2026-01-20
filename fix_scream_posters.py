import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from films.models import Film


class Command(BaseCommand):
    help = 'Исправление постеров для серии Крик'

    def handle(self, *args, **options):
        self.stdout.write("🔪 ИСПРАВЛЕНИЕ ПОСТЕРОВ СЕРИИ КРИК")
        self.stdout.write("=" * 50)
        
        # Исправленные ссылки на постеры серии Крик
        scream_posters = {
            'Крик 2': 'https://upload.wikimedia.org/wikipedia/en/3/39/Scream_2_poster.jpg',
            'Крик 3': 'https://upload.wikimedia.org/wikipedia/en/4/4b/Scream_3_poster.jpg',
            'Крик 4': 'https://upload.wikimedia.org/wikipedia/en/7/7b/Scream_4_poster.jpg',
            'Крик 5': 'https://upload.wikimedia.org/wikipedia/en/8/8f/Scream_%282022_film%29_poster.jpg',
            'Крик 6': 'https://upload.wikimedia.org/wikipedia/en/3/3b/Scream_VI_poster.jpg'
        }
        
        success_count = 0
        error_count = 0
        
        for title, url in scream_posters.items():
            try:
                film = Film.objects.get(title=title)
                self.stdout.write(f"🔪 Загружаю постер для '{title}'...")
                
                # Загружаем изображение
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                # Создаем имя файла
                filename = f"{title.lower().replace(' ', '_')}_poster.jpg"
                
                # Сохраняем файл
                film.poster.save(
                    filename,
                    ContentFile(response.content),
                    save=True
                )
                
                self.stdout.write(self.style.SUCCESS(f"  ✅ Постер для '{title}' загружен"))
                success_count += 1
                
            except Film.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"  ❌ Фильм '{title}' не найден"))
                error_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ❌ Ошибка загрузки постера для '{title}': {e}"))
                error_count += 1
        
        self.stdout.write(f"\n📊 СТАТИСТИКА КРИК:")
        self.stdout.write(f"  ✅ Успешно загружено: {success_count}")
        self.stdout.write(f"  ❌ Ошибок: {error_count}")
        
        if success_count > 0:
            self.stdout.write(self.style.SUCCESS(f"\n🔪 ПОСТЕРЫ КРИК ИСПРАВЛЕНЫ!"))
            self.stdout.write("🖼️ Теперь у всех фильмов серии Крик есть постеры")
        
        # Проверим общую статистику
        total_films = Film.objects.count()
        films_with_posters = Film.objects.exclude(poster='').count()
        
        self.stdout.write(f"\n📈 ОБЩАЯ СТАТИСТИКА:")
        self.stdout.write(f"  📁 Всего фильмов: {total_films}")
        self.stdout.write(f"  🖼️ С постерами: {films_with_posters}")
        self.stdout.write(f"  📊 Покрытие: {(films_with_posters/total_films*100):.1f}%")
        
        if films_with_posters == total_films:
            self.stdout.write(self.style.SUCCESS(f"\n🎉 ВСЕ ПОСТЕРЫ ЗАГРУЖЕНЫ!"))
            self.stdout.write("🎬 TochkaFilms теперь с оригинальными постерами!")
        else:
            missing = total_films - films_with_posters
            self.stdout.write(self.style.WARNING(f"\n⚠️ Осталось загрузить: {missing} постеров"))
        
        self.stdout.write(f"\n🔪 КРИК - ПОСТЕРЫ ГОТОВЫ!")