from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Исправляет проблемы с Rutube трейлерами'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Исправление Rutube трейлеров...")
        
        # Вместо несуществующих Rutube ссылок используем рабочие альтернативы
        # Или создаем красивые заглушки с переходом на официальные сайты
        
        working_trailers = {
            # Используем рабочие YouTube embed как временное решение
            # В реальном проекте замените на настоящие VK/Rutube ссылки
            'Начало': 'https://www.youtube.com/embed/YoHD9XEInc0',
            'Интерстеллар': 'https://www.youtube.com/embed/zSWdZVtXT7E', 
            'Темный рыцарь': 'https://www.youtube.com/embed/EXeTwQWrcwY',
            'Побег из Шоушенка': 'https://www.youtube.com/embed/6hB3S9bIaco',
            'Форрест Гамп': 'https://www.youtube.com/embed/bLvqoHBptjg',
            'Матрица': 'https://www.youtube.com/embed/vKQi3bIA1HI',
            'Криминальное чтиво': 'https://www.youtube.com/embed/s7EdQ4FqbhY',
            'Бойцовский клуб': 'https://www.youtube.com/embed/qtRKdVHc-cE',
            'Джон Уик': 'https://www.youtube.com/embed/C0BMx-qxsP4',
            'Мстители: Финал': 'https://www.youtube.com/embed/TcMBFSGVi1c',
            'Джокер': 'https://www.youtube.com/embed/zAGVQLHvwOY',
            'Паразиты': 'https://www.youtube.com/embed/5xH0HfJHsaY',
            'Дюна': 'https://www.youtube.com/embed/n9xhJrPXop4',
        }
        
        # Альтернативный подход - убираем embed и показываем только кнопки перехода
        external_links = {
            'Начало': 'https://www.kinopoisk.ru/film/447301/',
            'Интерстеллар': 'https://www.kinopoisk.ru/film/258687/',
            'Темный рыцарь': 'https://www.kinopoisk.ru/film/111543/',
            'Побег из Шоушенка': 'https://www.kinopoisk.ru/film/326/',
            'Форрест Гамп': 'https://www.kinopoisk.ru/film/448/',
            'Матрица': 'https://www.kinopoisk.ru/film/301/',
            'Криминальное чтиво': 'https://www.kinopoisk.ru/film/342/',
            'Бойцовский клуб': 'https://www.kinopoisk.ru/film/361/',
            'Джон Уик': 'https://www.kinopoisk.ru/film/762738/',
            'Мстители: Финал': 'https://www.kinopoisk.ru/film/843650/',
            'Джокер': 'https://www.kinopoisk.ru/film/1108577/',
            'Паразиты': 'https://www.kinopoisk.ru/film/1043758/',
            'Дюна': 'https://www.kinopoisk.ru/film/1100777/',
        }
        
        choice = input("Выберите решение:\n1. Рабочие YouTube трейлеры\n2. Ссылки на КиноПоиск\n3. Убрать трейлеры для проблемных фильмов\nВведите номер (1-3): ")
        
        if choice == "1":
            self.stdout.write("🎬 Устанавливаем рабочие YouTube трейлеры...")
            trailers_to_use = working_trailers
            platform_name = "YouTube (рабочие)"
        elif choice == "2":
            self.stdout.write("🔗 Устанавливаем ссылки на КиноПоиск...")
            trailers_to_use = external_links
            platform_name = "КиноПоиск"
        else:
            self.stdout.write("❌ Убираем трейлеры для проблемных фильмов...")
            # Убираем трейлеры у фильмов с Rutube
            rutube_films = Film.objects.filter(trailer_url__contains='rutube.ru')
            for film in rutube_films:
                film.trailer_url = ''
                film.save()
                self.stdout.write(f"  ❌ Убран трейлер: {film.title}")
            
            self.stdout.write(self.style.SUCCESS(f"\n✅ Убрано {rutube_films.count()} проблемных трейлеров"))
            return
        
        updated_count = 0
        
        for title, url in trailers_to_use.items():
            try:
                film = Film.objects.get(title=title)
                film.trailer_url = url
                film.save()
                
                self.stdout.write(f"  ✅ {title} -> {platform_name}")
                updated_count += 1
                
            except Film.DoesNotExist:
                self.stdout.write(f"  ❌ Фильм '{title}' не найден")
        
        self.stdout.write(
            self.style.SUCCESS(f"\n🎉 Обновлено {updated_count} трейлеров")
        )
        
        # Показываем итоговую статистику
        vk_count = Film.objects.filter(trailer_url__contains='vk.com').count()
        youtube_count = Film.objects.filter(trailer_url__contains='youtube.com').count()
        kinopoisk_count = Film.objects.filter(trailer_url__contains='kinopoisk.ru').count()
        
        self.stdout.write(f"\n📊 Итоговая статистика:")
        self.stdout.write(f"  📺 VK Video: {vk_count}")
        self.stdout.write(f"  📺 YouTube: {youtube_count}")
        self.stdout.write(f"  🔗 КиноПоиск: {kinopoisk_count}")
        
        if choice == "1":
            self.stdout.write("\n💡 YouTube трейлеры работают стабильно")
            self.stdout.write("   В будущем замените на настоящие VK/Rutube")
        elif choice == "2":
            self.stdout.write("\n💡 Ссылки ведут на официальные страницы фильмов")
            self.stdout.write("   Пользователи смогут найти трейлеры там")
        
        self.stdout.write(self.style.SUCCESS("\n🔧 Проблема с Rutube решена!"))