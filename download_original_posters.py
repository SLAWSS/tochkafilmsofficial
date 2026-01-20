import os
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from films.models import Film


class Command(BaseCommand):
    help = 'Загрузка оригинальных постеров фильмов'

    def handle(self, *args, **options):
        self.stdout.write("🎬 ЗАГРУЗКА ОРИГИНАЛЬНЫХ ПОСТЕРОВ")
        self.stdout.write("=" * 50)
        
        # Словарь с прямыми ссылками на оригинальные постеры
        poster_urls = {
            'Начало': 'https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg',
            'Интерстеллар': 'https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg',
            'Темный рыцарь': 'https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg',
            'Побег из Шоушенка': 'https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_SX300.jpg',
            'Форрест Гамп': 'https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg',
            'Матрица': 'https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg',
            'Криминальное чтиво': 'https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg',
            'Бойцовский клуб': 'https://m.media-amazon.com/images/M/MV5BNDIzNDU0YzEtYzE5Ni00ZjlkLTk5ZjgtNjM3NWE4YzA3Nzk3XkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_SX300.jpg',
            'Крик': 'https://m.media-amazon.com/images/M/MV5BMjA2NjU5MTg5OF5BMl5BanBnXkFtZTgwOTkyMzQxMDE@._V1_SX300.jpg',
            'Крик 2': 'https://m.media-amazon.com/images/M/MV5BNDcyNDA4NDAzN15BMl5BanBnXkFtZTgwODQyMzQxMDE@._V1_SX300.jpg',
            'Крик 3': 'https://m.media-amazon.com/images/M/MV5BMjM5NjEyMzA4MF5BMl5BanBnXkFtZTgwNDQyMzQxMDE@._V1_SX300.jpg',
            'Крик 4': 'https://m.media-amazon.com/images/M/MV5BMjEwNTg1MzAyNl5BMl5BanBnXkFtZTcwMzEyMDIwNQ@@._V1_SX300.jpg',
            'Крик 5': 'https://m.media-amazon.com/images/M/MV5BYTdkN2YzYTQtZjNhZC00YjlmLWI2OWMtYjYwMWQzOGQ1MjVkXkEyXkFqcGdeQXVyMTEyMjM2NDc2._V1_SX300.jpg',
            'Крик 6': 'https://m.media-amazon.com/images/M/MV5BMjM0NTc0NzItM2FlYS00MzBhLWFlNzMtNzUyNTkzNGQ1MjY2XkEyXkFqcGdeQXVyMTUzMTg2ODkz._V1_SX300.jpg',
            'Джон Уик': 'https://m.media-amazon.com/images/M/MV5BMTU2NjA1ODgzMF5BMl5BanBnXkFtZTgwMTM2MTI4MjE@._V1_SX300.jpg',
            'Мстители: Финал': 'https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_SX300.jpg',
            'Джокер': 'https://m.media-amazon.com/images/M/MV5BNGVjNWI4ZGUtNzE0MS00YTJmLWE0ZDctN2ZiYTk2YmI3NTYyXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_SX300.jpg',
            'Паразиты': 'https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_SX300.jpg',
            'Дюна': 'https://m.media-amazon.com/images/M/MV5BN2FjNmEyNWMtYzM0ZS00NjIyLTg5YzYtYThlMGVjNzE1OGViXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_SX300.jpg',
            'Оно': 'https://m.media-amazon.com/images/M/MV5BZDVkZmI0YzAtNzdjYi00ZjhhLWE1ODEtMWMzMWMzNDA0NmQ4XkEyXkFqcGdeQXVyNzYzODM3Mzg@._V1_SX300.jpg'
        }
        
        success_count = 0
        error_count = 0
        
        for film in Film.objects.all():
            if film.title in poster_urls:
                try:
                    self.stdout.write(f"📥 Загружаю постер для '{film.title}'...")
                    
                    # Загружаем изображение
                    response = requests.get(poster_urls[film.title], timeout=30)
                    response.raise_for_status()
                    
                    # Создаем имя файла
                    filename = f"{film.title.lower().replace(' ', '_').replace(':', '')}_poster.jpg"
                    
                    # Сохраняем файл
                    film.poster.save(
                        filename,
                        ContentFile(response.content),
                        save=True
                    )
                    
                    self.stdout.write(self.style.SUCCESS(f"  ✅ Постер для '{film.title}' загружен"))
                    success_count += 1
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  ❌ Ошибка загрузки постера для '{film.title}': {e}"))
                    error_count += 1
            else:
                self.stdout.write(self.style.WARNING(f"  ⚠️ Постер для '{film.title}' не найден в базе"))
                error_count += 1
        
        self.stdout.write(f"\n📊 СТАТИСТИКА:")
        self.stdout.write(f"  ✅ Успешно загружено: {success_count}")
        self.stdout.write(f"  ❌ Ошибок: {error_count}")
        self.stdout.write(f"  📁 Всего фильмов: {Film.objects.count()}")
        
        if success_count > 0:
            self.stdout.write(self.style.SUCCESS(f"\n🎉 ПОСТЕРЫ ЗАГРУЖЕНЫ!"))
            self.stdout.write("🖼️ Теперь у фильмов есть оригинальные постеры")
            self.stdout.write("🌐 Откройте сайт чтобы увидеть результат")
        else:
            self.stdout.write(self.style.ERROR(f"\n❌ НЕ УДАЛОСЬ ЗАГРУЗИТЬ ПОСТЕРЫ"))
            self.stdout.write("🔧 Проверьте интернет соединение и попробуйте снова")
        
        self.stdout.write(f"\n🎬 TOCHKAFILMS - ОРИГИНАЛЬНЫЕ ПОСТЕРЫ!")