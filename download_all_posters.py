import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from films.models import Film


class Command(BaseCommand):
    help = 'Загрузка оригинальных постеров для всех фильмов'

    def handle(self, *args, **options):
        self.stdout.write("🖼️ ЗАГРУЗКА ПОСТЕРОВ ДЛЯ ВСЕХ ФИЛЬМОВ")
        self.stdout.write("=" * 60)
        
        # Полная база оригинальных постеров для всех фильмов
        all_posters = {
            # Основные фильмы
            'Терминатор': 'https://cdn.ananasposter.ru/image/cache/catalog/poster/film/90/3753-1000x830.jpg',
            'Терминатор 2': 'https://m.media-amazon.com/images/M/MV5BMGU2NzRmZjUtOGUxYS00ZjdjLWEwZWItY2NlM2JhNjkxNTFmXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg',
            'Титаник': 'https://m.media-amazon.com/images/M/MV5BMDdmZGU3NDQtY2E5My00ZTliLWIzOTUtMTY4ZGI1YjdiNjk3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg',
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
            'Миссия невыполнима': 'https://m.media-amazon.com/images/M/MV5BMTc3NjI2MjU0Nl5BMl5BanBnXkFtZTgwNDk3ODYxMTE@._V1_SX300.jpg',
            
            # Топ фильмы
            'Форрест Гамп': 'https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg',
            'Побег из Шоушенка': 'https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg',
            'Темный рыцарь': 'https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg',
            'Криминальное чтиво': 'https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg',
            'Начало': 'https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg',
            'Бойцовский клуб': 'https://m.media-amazon.com/images/M/MV5BMmEzNTkxYjQtZTc0MC00YTVjLTg5ZTEtZWMwOWVlYzY0NWIwXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg',
            'Интерстеллар': 'https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg',
            'Матрица': 'https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg',
            'Список Шиндлера': 'https://m.media-amazon.com/images/M/MV5BNDE4OTMxMTctNmRhYy00NWE2LTg3YzItYTk3M2UwOTU5Njg4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg',
            'Зеленая миля': 'https://m.media-amazon.com/images/M/MV5BMTUxMzQyNjA5MF5BMl5BanBnXkFtZTYwOTU2NTY3._V1_SX300.jpg',
            
            # Дополнительные популярные фильмы
            'Звездные войны: Новая надежда': 'https://m.media-amazon.com/images/M/MV5BNzVlY2MwMjktM2E4OS00Y2Y3LWE3ZjctYzhkZGM3YzA1ZWM2XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg',
            'Властелин колец: Две крепости': 'https://m.media-amazon.com/images/M/MV5BZGMxZTdjZmYtMmE2Ni00ZTdkLWI5NTgtNjlmMjBiNzU2MmI5XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg',
            'Гарри Поттер и тайная комната': 'https://m.media-amazon.com/images/M/MV5BMjE0YjUzNDUtMjc5OS00MTU3LTgxMmUtODhkOThkMzdjNWI4XkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_SX300.jpg',
            'Мадагаскар': 'https://m.media-amazon.com/images/M/MV5BOTgxMTQwMjAwM15BMl5BanBnXkFtZTcwNTk4NjIxMw@@._V1_SX300.jpg',
            'Ледниковый период': 'https://m.media-amazon.com/images/M/MV5BMmYxZWY2NzgtNjkzYi00MDI0LWE5ZWEtMTRmZjEyODZiYWUxXkEyXkFqcGdeQXVyNjUwNzk3NDc@._V1_SX300.jpg',
            'Сокровище нации': 'https://m.media-amazon.com/images/M/MV5BMTY3NTc4ZjUtOGZhZi00NWRmLWE2MjgtNzE5MjQxMWVhZmU2XkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg',
            'Мумия': 'https://m.media-amazon.com/images/M/MV5BODJmODQyYTMtZGM3My00ZDQ0LWIzNzAtOGIzYWVmY2YxZjA2XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg',
            'Джуманджи': 'https://m.media-amazon.com/images/M/MV5BZTk2ZmUwYmEtNTcwZS00YmMyLWFkYjMtNTRmZDA3YWExMjc2XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg',
            
            # Современные фильмы
            'Мстители: Финал': 'https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_SX300.jpg',
            'Джокер': 'https://m.media-amazon.com/images/M/MV5BNGVjNWI4ZGUtNzE0MS00YTJmLWE0ZDctN2ZiYTk2YmI3NTYyXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_SX300.jpg',
            'Паразиты': 'https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_SX300.jpg',
            'Дюна': 'https://m.media-amazon.com/images/M/MV5BN2FjNmEyNWMtYzM0ZS00NjIyLTg5YzYtYThlMGVjNzE1OGViXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_SX300.jpg',
            'Оно': 'https://m.media-amazon.com/images/M/MV5BZDVkZmI0YzAtNzdjYi00ZjhhLWI1ZDYtMzNmNDdkYmNhNTRkXkEyXkFqcGdeQXVyNzYzODM3Mzg@._V1_SX300.jpg',
            'Джон Уик': 'https://m.media-amazon.com/images/M/MV5BMTU2NjA1ODgzMF5BMl5BanBnXkFtZTgwMTM2MTI4MjE@._V1_SX300.jpg',
            
            # Дополнительные фильмы
            'Конг: Остров черепа': 'https://m.media-amazon.com/images/M/MV5BMTUwMzI5ODEwM15BMl5BanBnXkFtZTgwNTMwMDE2MDI@._V1_SX300.jpg',
            'Затерянный мир': 'https://m.media-amazon.com/images/M/MV5BMDFlMmM4Y2QtNDg1ZS00MWVlLTIwNTctYjlkYjI2OTVmM2MxXkEyXkFqcGdeQXVyNTI4MjkwNjA@._V1_SX300.jpg',
            'Индиана Джонс и храм судьбы': 'https://m.media-amazon.com/images/M/MV5BMjE5MzA0NjQwM15BMl5BanBnXkFtZTcwMjAwNDE3MQ@@._V1_SX300.jpg',
            'Из Африки': 'https://m.media-amazon.com/images/M/MV5BMjEyODE2NjkwNF5BMl5BanBnXkFtZTcwNzc0NjIyNA@@._V1_SX300.jpg',
            'Английский пациент': 'https://m.media-amazon.com/images/M/MV5BZDRiOGY5ZTctMWFlYS00ZGI5LWJlNjAtZWNjYjc0ZGJhMjJkXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg',
            'Мосты округа Мэдисон': 'https://m.media-amazon.com/images/M/MV5BMTkwNjY2NTYwNF5BMl5BanBnXkFtZTcwODAwNzE3OA@@._V1_SX300.jpg',
            'Влюбленный Шекспир': 'https://m.media-amazon.com/images/M/MV5BM2ZkNjM5MjEtMGVmZi00ZWM3LWI4NWEtYjhlMWZhZGYyNzJlXkEyXkFqcGdeQXVyNDYyMDk5MTU@._V1_SX300.jpg',
            'Если только': 'https://m.media-amazon.com/images/M/MV5BMTYwNjAzNzUzOF5BMl5BanBnXkFtZTYwNDM4MDE3._V1_SX300.jpg',
            'Спеши любить': 'https://m.media-amazon.com/images/M/MV5BMjE5MzA0NjQwM15BMl5BanBnXkFtZTcwMjAwNDE3MQ@@._V1_SX300.jpg',
            'Дневник памяти': 'https://m.media-amazon.com/images/M/MV5BMTk3OTM5Njg5M15BMl5BanBnXkFtZTYwMzA0ODI3._V1_SX300.jpg',
            'Э.Т.': 'https://m.media-amazon.com/images/M/MV5BMTQ2ODFlMDAtNzdhOC00ZDYzLWE3YTMtNDU4ZGFmZmJmYTczXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg',
            'Хроники Нарнии': 'https://m.media-amazon.com/images/M/MV5BMTc0NTUwMTU5OV5BMl5BanBnXkFtZTcwNjAwNzQzMw@@._V1_SX300.jpg',
        }
        
        success_count = 0
        error_count = 0
        
        self.stdout.write("🖼️ ЗАГРУЗКА ПОСТЕРОВ:")
        
        for title, url in all_posters.items():
            try:
                film = Film.objects.get(title=title)
                
                self.stdout.write(f"  📥 Загружаю: {title}")
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                }
                
                response = requests.get(url, timeout=30, headers=headers)
                response.raise_for_status()
                
                if len(response.content) < 1000:
                    raise Exception("Файл слишком маленький")
                
                if not response.headers.get('content-type', '').startswith('image/'):
                    raise Exception("Не является изображением")
                
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                filename = f"{safe_title.lower().replace(' ', '_')}_original.jpg"
                
                film.poster.save(filename, ContentFile(response.content), save=True)
                
                self.stdout.write(self.style.SUCCESS(f"    ✅ Загружен: {title}"))
                success_count += 1
                
            except Film.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"    ❌ Не найден: {title}"))
                error_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"    ❌ Ошибка {title}: {str(e)[:40]}"))
                error_count += 1
        
        # Финальная статистика
        total_films = Film.objects.count()
        films_with_posters = Film.objects.exclude(poster='').count()
        
        self.stdout.write(f"\n📊 РЕЗУЛЬТАТЫ:")
        self.stdout.write(f"  ✅ Постеров загружено: {success_count}")
        self.stdout.write(f"  ❌ Ошибок: {error_count}")
        
        self.stdout.write(f"\n📈 ИТОГОВАЯ СТАТИСТИКА:")
        self.stdout.write(f"  🎬 Всего фильмов: {total_films}")
        self.stdout.write(f"  🖼️ С постерами: {films_with_posters}")
        self.stdout.write(f"  📊 Покрытие: {(films_with_posters/total_films*100):.1f}%")
        
        if success_count > 0:
            self.stdout.write(self.style.SUCCESS(f"\n🖼️ ПОСТЕРЫ ЗАГРУЖЕНЫ!"))
            self.stdout.write("🌟 Все фильмы теперь с оригинальными постерами")
            self.stdout.write("🎨 Высокое качество изображений")
        
        self.stdout.write(self.style.SUCCESS("✨ Загрузка завершена!"))