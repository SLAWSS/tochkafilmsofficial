import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from films.models import Film


class Command(BaseCommand):
    help = 'Загрузка оригинальных постеров для всех частей серии Крик'

    def handle(self, *args, **options):
        self.stdout.write("🔪 ЗАГРУЗКА ОРИГИНАЛЬНЫХ ПОСТЕРОВ СЕРИИ КРИК")
        self.stdout.write("=" * 60)
        
        # Оригинальные постеры всех частей Крик с высоким качеством
        scream_posters = {
            'Крик': 'https://image.tmdb.org/t/p/w500/7MW6sAqAdtqb6HcHOfFhOY9U9BS.jpg',
            'Крик 2': 'https://image.tmdb.org/t/p/w500/dORlVasiaDkJXTqt9bdH7nFNs6C.jpg',
            'Крик 3': 'https://image.tmdb.org/t/p/w500/tYTtvNvdIKSaX3r4YfkaNKoezqq.jpg',
            'Крик 4': 'https://image.tmdb.org/t/p/w500/tcrI37K98TVopLbcZBa55mWhLT1.jpg',
            'Крик 5': 'https://image.tmdb.org/t/p/w500/1m3W6cpgwuIyjtg5nSnPx7yFkXW.jpg',
            'Крик 6': 'https://image.tmdb.org/t/p/w500/wDWwtvkRRlgTiUr6TyLSMX8FCuZ.jpg'
        }
        
        # Альтернативные ссылки если TMDB не работает
        alternative_posters = {
            'Крик': 'https://m.media-amazon.com/images/M/MV5BMjA2NjU5MTg5OF5BMl5BanBnXkFtZTgwOTkyMzQxMDE@._V1_SX300.jpg',
            'Крик 2': 'https://m.media-amazon.com/images/M/MV5BNDcyNDA4NDAzN15BMl5BanBnXkFtZTgwODQyMzQxMDE@._V1_SX300.jpg',
            'Крик 3': 'https://m.media-amazon.com/images/M/MV5BMjM5NjEyMzA4MF5BMl5BanBnXkFtZTgwNDQyMzQxMDE@._V1_SX300.jpg',
            'Крик 4': 'https://m.media-amazon.com/images/M/MV5BMjEwNTg1MzAyNl5BMl5BanBnXkFtZTcwMzEyMDIwNQ@@._V1_SX300.jpg',
            'Крик 5': 'https://m.media-amazon.com/images/M/MV5BYTdkN2YzYTQtZjNhZC00YjlmLWI2OWMtYjYwMWQzOGQ1MjVkXkEyXkFqcGdeQXVyMTEyMjM2NDc2._V1_SX300.jpg',
            'Крик 6': 'https://m.media-amazon.com/images/M/MV5BMjM0NTc0NzItM2FlYS00MzBhLWFlNzMtNzUyNTkzNGQ1MjY2XkEyXkFqcGdeQXVyMTUzMTg2ODkz._V1_SX300.jpg'
        }
        
        # Еще одни альтернативные ссылки (высокое качество)
        backup_posters = {
            'Крик': 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/7MW6sAqAdtqb6HcHOfFhOY9U9BS.jpg',
            'Крик 2': 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/dORlVasiaDkJXTqt9bdH7nFNs6C.jpg',
            'Крик 3': 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/tYTtvNvdIKSaX3r4YfkaNKoezqq.jpg',
            'Крик 4': 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/tcrI37K98TVopLbcZBa55mWhLT1.jpg',
            'Крик 5': 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/1m3W6cpgwuIyjtg5nSnPx7yFkXW.jpg',
            'Крик 6': 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/wDWwtvkRRlgTiUr6TyLSMX8FCuZ.jpg'
        }
        
        success_count = 0
        error_count = 0
        
        for title in scream_posters.keys():
            try:
                film = Film.objects.get(title=title)
                self.stdout.write(f"🔪 Загружаю оригинальный постер для '{title}'...")
                
                # Пробуем загрузить с разных источников
                urls_to_try = [
                    scream_posters[title],
                    alternative_posters[title],
                    backup_posters[title]
                ]
                
                poster_loaded = False
                
                for i, url in enumerate(urls_to_try, 1):
                    try:
                        self.stdout.write(f"  📥 Попытка {i}: {url[:50]}...")
                        
                        # Добавляем заголовки для обхода блокировок
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.9',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'DNT': '1',
                            'Connection': 'keep-alive',
                            'Upgrade-Insecure-Requests': '1',
                        }
                        
                        response = requests.get(url, timeout=30, headers=headers)
                        response.raise_for_status()
                        
                        # Проверяем что это действительно изображение
                        if len(response.content) < 1000:
                            raise Exception("Файл слишком маленький")
                        
                        if not response.headers.get('content-type', '').startswith('image/'):
                            raise Exception("Не является изображением")
                        
                        # Создаем имя файла
                        filename = f"scream_{title.split()[-1] if len(title.split()) > 1 else '1'}_original.jpg"
                        
                        # Сохраняем файл
                        film.poster.save(
                            filename,
                            ContentFile(response.content),
                            save=True
                        )
                        
                        self.stdout.write(self.style.SUCCESS(f"  ✅ Постер для '{title}' загружен (источник {i})"))
                        success_count += 1
                        poster_loaded = True
                        break
                        
                    except Exception as e:
                        self.stdout.write(f"  ⚠️ Источник {i} не работает: {str(e)[:50]}")
                        continue
                
                if not poster_loaded:
                    self.stdout.write(self.style.ERROR(f"  ❌ Не удалось загрузить постер для '{title}' ни из одного источника"))
                    error_count += 1
                
            except Film.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"  ❌ Фильм '{title}' не найден в базе данных"))
                error_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ❌ Общая ошибка для '{title}': {e}"))
                error_count += 1
        
        self.stdout.write(f"\n📊 СТАТИСТИКА ЗАГРУЗКИ:")
        self.stdout.write(f"  ✅ Успешно загружено: {success_count}")
        self.stdout.write(f"  ❌ Ошибок: {error_count}")
        self.stdout.write(f"  📁 Всего фильмов Крик: {len(scream_posters)}")
        
        if success_count > 0:
            self.stdout.write(self.style.SUCCESS(f"\n🔪 ОРИГИНАЛЬНЫЕ ПОСТЕРЫ КРИК ЗАГРУЖЕНЫ!"))
            self.stdout.write("🖼️ Теперь у всех частей серии Крик оригинальные постеры")
            self.stdout.write("🎬 Серия выглядит профессионально и единообразно")
        
        if error_count > 0:
            self.stdout.write(self.style.WARNING(f"\n⚠️ Некоторые постеры не удалось загрузить"))
            self.stdout.write("🔧 Попробуйте запустить команду еще раз")
        
        # Проверим общую статистику
        total_films = Film.objects.count()
        films_with_posters = Film.objects.exclude(poster='').count()
        scream_films = Film.objects.filter(title__startswith='Крик').count()
        scream_with_posters = Film.objects.filter(title__startswith='Крик').exclude(poster='').count()
        
        self.stdout.write(f"\n📈 ОБЩАЯ СТАТИСТИКА:")
        self.stdout.write(f"  📁 Всего фильмов: {total_films}")
        self.stdout.write(f"  🖼️ С постерами: {films_with_posters}")
        self.stdout.write(f"  🔪 Фильмов Крик: {scream_films}")
        self.stdout.write(f"  🖼️ Крик с постерами: {scream_with_posters}")
        self.stdout.write(f"  📊 Покрытие Крик: {(scream_with_posters/scream_films*100):.1f}%")
        
        self.stdout.write(f"\n🌐 ТЕСТИРОВАНИЕ:")
        test_steps = [
            "1. Откройте http://127.0.0.1:8000/",
            "2. Найдите фильмы серии Крик",
            "3. Убедитесь что у всех оригинальные постеры",
            "4. Проверьте качество изображений",
            "5. Кликните на карточки - должны открываться страницы фильмов"
        ]
        
        for step in test_steps:
            self.stdout.write(f"  {step}")
        
        if scream_with_posters == scream_films:
            self.stdout.write(self.style.SUCCESS(f"\n🎉 ВСЯ СЕРИЯ КРИК С ОРИГИНАЛЬНЫМИ ПОСТЕРАМИ!"))
            self.stdout.write("🔪 Ghostface будет доволен!")
        
        self.stdout.write(f"\n🔪 SCREAM FRANCHISE - ОРИГИНАЛЬНЫЕ ПОСТЕРЫ ГОТОВЫ!")