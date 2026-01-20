import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from films.models import Film


class Command(BaseCommand):
    help = 'Загрузка дополнительных оригинальных постеров'

    def handle(self, *args, **options):
        self.stdout.write("🖼️ ЗАГРУЗКА ДОПОЛНИТЕЛЬНЫХ ПОСТЕРОВ")
        self.stdout.write("=" * 60)
        
        # Дополнительные постеры для популярных фильмов
        additional_posters = {
            'Терминатор': 'https://m.media-amazon.com/images/M/MV5BYTViNzMxZjEtZGEwNy00MDNiLWIzNGQtZDY2MjQ1OWViZjFmXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg',
            'Терминатор 2': 'https://m.media-amazon.com/images/M/MV5BMGU2NzRmZjUtOGUxYS00ZjdjLWEwZWItY2NlM2JhNjkxNTFmXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg',
            'Титаник': 'https://m.media-amazon.com/images/M/MV5BMDdmZGU3NDQtY2E5My00ZTliLWIzOTUtMTY4ZGI1YjdiNjk3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg',
            'Звездные войны: Новая надежда': 'https://m.media-amazon.com/images/M/MV5BNzVlY2MwMjktM2E4OS00Y2Y3LWE3ZjctYzhkZGM3YzA1ZWM2XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg',
            'Назад в будущее': 'https://m.media-amazon.com/images/M/MV5BZmU0M2Y1OGUtZjIxNi00ZjBkLTg1MjgtOWIyNThiZWIwYjRiXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg',
            'Чужой': 'https://m.media-amazon.com/images/M/MV5BOGQzZTBjMjQtOTVmMS00NGE5LWEyYmMtOGQ1ZGZjNmRkYjFhXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_SX300.jpg',
            'Парк Юрского периода': 'https://m.media-amazon.com/images/M/MV5BMjM2MDgxMDg0Nl5BMl5BanBnXkFtZTgwNTM2OTM5NDE@._V1_SX300.jpg',
            'Король Лев': 'https://m.media-amazon.com/images/M/MV5BYTYxNGMyZTYtMjE3MS00MzNjLWFjNmYtMDk3N2FmM2JiM2M1XkEyXkFqcGdeQXVyNjY5NDU4NzI@._V1_SX300.jpg',
            'История игрушек': 'https://m.media-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2OTk4MzI@._V1_SX300.jpg',
            'Гладиатор': 'https://m.media-amazon.com/images/M/MV5BMDliMmNhNDEtODUyOS00MjNlLTgxODEtN2U3NzIxMGVkZTA1L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg',
            'Властелин колец: Братство кольца': 'https://m.media-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWI0NTctMzY4M2VlOTdjZWRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_SX300.jpg',
            'Гарри Поттер и философский камень': 'https://m.media-amazon.com/images/M/MV5BNjQ3NWNlNmQtMTE5ZS00MDdmLTlkZjUtZTBlM2UxMGFiMTU3XkEyXkFqcGdeQXVyNjUwNzk3NDc@._V1_SX300.jpg',
            'В поисках Немо': 'https://m.media-amazon.com/images/M/MV5BZjMxYzc4MzEtZDg4MS00N2Q5LWJlMzEtNTBlNGZiOWM5NzNlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg',
            'Шрек': 'https://m.media-amazon.com/images/M/MV5BOGZhM2FhNTItODAzNi00YjA0LWEyN2UtNjJlYWQzYzU1MDg5L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg',
            'Пираты Карибского моря': 'https://m.media-amazon.com/images/M/MV5BNGYyZGM5MGMtYTY2Ni00M2Y1LWIzNjQtYWUzM2VlNGVhMDNhXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg',
            'Один дома': 'https://m.media-amazon.com/images/M/MV5BMzFkM2YwOTQtYzk2Mi00N2VlLWE3NTItN2YwNDg1YmY0ZDNmXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg',
            'Маска': 'https://m.media-amazon.com/images/M/MV5BOTdjZGVkNjgtYzgxMS00OTBjLTk1ODAtMTMxYjY3ODg0OTBkXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg',
            'Молчание ягнят': 'https://m.media-amazon.com/images/M/MV5BNjNhZTk0ZmEtNjJhMi00YzFlLWE1MmEtYzM1M2ZmMGMwMTU4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg',
            'Семь': 'https://m.media-amazon.com/images/M/MV5BOTUwODM5MTctZjczMi00OTk4LTg3NWUtNmVhMTAzNTNjYjcyXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg',
            'Экзорцист': 'https://m.media-amazon.com/images/M/MV5BYWFlZGY2NDktY2ZjOS00ZWNkLTg0ZDAtZDY4MTM1ODU4ZjljXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_SX300.jpg',
            'Сияние': 'https://m.media-amazon.com/images/M/MV5BZWFlYmY2MGEtZjVkYS00YzU4LTg0YjQtYzY1ZGE3NTA5NGQxXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg',
            'Психо': 'https://m.media-amazon.com/images/M/MV5BNTQwNDM1YzItNDAxZC00NWY2LTk0M2UtNDIwNWI5OGUyNWUxXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg',
            'Красотка': 'https://m.media-amazon.com/images/M/MV5BMjE5ODk5NjcxNl5BMl5BanBnXkFtZTcwNjU2NjY5Nw@@._V1_SX300.jpg',
            'Грязные танцы': 'https://m.media-amazon.com/images/M/MV5BMzM1ZDY0OWUtOTY2MS00MmIzLWEwNmMtZmZlNGVmNjA3Y2I4XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg',
            'Призрак': 'https://m.media-amazon.com/images/M/MV5BMTM0NDM0MzMzOV5BMl5BanBnXkFtZTcwMDQzODMzNA@@._V1_SX300.jpg',
            'Индиана Джонс: В поисках утраченного ковчега': 'https://m.media-amazon.com/images/M/MV5BMjA0ODEzMTc1Nl5BMl5BanBnXkFtZTcwODM2MjAxNA@@._V1_SX300.jpg',
            'Крепкий орешек': 'https://m.media-amazon.com/images/M/MV5BZjRlNDUxZjAtOGQ4OC00OTNlLTgwNWMtYTBmMWI3ZGI0OGMwXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg',
            'Скорость': 'https://m.media-amazon.com/images/M/MV5BYjc0MjYyNDctZGVmZi00NzY0LWIwYWUtZWVmNjQ5M2I5ZjMwXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg',
            'Миссия невыполнима': 'https://m.media-amazon.com/images/M/MV5BMTc3NjI2MjU0Nl5BMl5BanBnXkFtZTgwNDk3ODYxMTE@._V1_SX300.jpg'
        }
        
        success_count = 0
        error_count = 0
        
        for title, url in additional_posters.items():
            try:
                film = Film.objects.get(title=title)
                
                # Проверяем, есть ли уже оригинальный постер
                if film.poster and 'poster.jpg' in film.poster.name:
                    self.stdout.write(f"  ℹ️ У '{title}' уже есть оригинальный постер")
                    continue
                
                self.stdout.write(f"🖼️ Загружаю постер для '{title}'...")
                
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
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                filename = f"{safe_title.lower().replace(' ', '_')}_original.jpg"
                
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
                self.stdout.write(self.style.ERROR(f"  ❌ Ошибка загрузки постера для '{title}': {str(e)[:50]}"))
                error_count += 1
        
        self.stdout.write(f"\n📊 СТАТИСТИКА ЗАГРУЗКИ:")
        self.stdout.write(f"  ✅ Успешно загружено: {success_count}")
        self.stdout.write(f"  ❌ Ошибок: {error_count}")
        
        # Общая статистика постеров
        total_films = Film.objects.count()
        films_with_posters = Film.objects.exclude(poster='').count()
        
        self.stdout.write(f"\n📈 ОБЩАЯ СТАТИСТИКА ПОСТЕРОВ:")
        self.stdout.write(f"  🎬 Всего фильмов: {total_films}")
        self.stdout.write(f"  🖼️ С постерами: {films_with_posters}")
        self.stdout.write(f"  📊 Покрытие: {(films_with_posters/total_films*100):.1f}%")
        
        if success_count > 0:
            self.stdout.write(self.style.SUCCESS(f"\n🖼️ ДОПОЛНИТЕЛЬНЫЕ ПОСТЕРЫ ЗАГРУЖЕНЫ!"))
            self.stdout.write("🌟 Коллекция стала еще красивее")
        
        self.stdout.write(self.style.SUCCESS("🎬 Загрузка завершена!"))