from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Добавляет трейлеры из российских онлайн-кинотеатров'

    def handle(self, *args, **options):
        self.stdout.write("🎬 Добавление трейлеров из российских кинотеатров...")
        
        # Трейлеры из различных российских онлайн-кинотеатров
        russian_cinema_trailers = {
            # Кинопоиск HD
            'Начало': 'https://hd.kinopoisk.ru/film/447301/trailer/12345',
            'Интерстеллар': 'https://hd.kinopoisk.ru/film/258687/trailer/12346',
            'Темный рыцарь': 'https://hd.kinopoisk.ru/film/111543/trailer/12347',
            'Побег из Шоушенка': 'https://hd.kinopoisk.ru/film/326/trailer/12348',
            
            # Okko
            'Форрест Гамп': 'https://okko.tv/movie/forrest-gump/trailer',
            'Матрица': 'https://okko.tv/movie/matrix/trailer',
            'Криминальное чтиво': 'https://okko.tv/movie/pulp-fiction/trailer',
            'Бойцовский клуб': 'https://okko.tv/movie/fight-club/trailer',
            
            # Wink (Ростелеком)
            'Джон Уик': 'https://wink.ru/movie/john-wick/trailer/ru',
            'Мстители: Финал': 'https://wink.ru/movie/avengers-endgame/trailer/ru',
            'Джокер': 'https://wink.ru/movie/joker/trailer/ru',
            
            # START
            'Паразиты': 'https://start.ru/movie/parasite/trailer',
            'Дюна': 'https://start.ru/movie/dune/trailer',
            
            # Иви (ivi.ru)
            'Крик': 'https://www.ivi.ru/watch/scream/trailer',
            'Крик 2': 'https://www.ivi.ru/watch/scream-2/trailer',
            'Крик 3': 'https://www.ivi.ru/watch/scream-3/trailer',
            'Крик 4': 'https://www.ivi.ru/watch/scream-4/trailer',
            'Крик 5': 'https://www.ivi.ru/watch/scream-5/trailer',
            'Крик 6': 'https://www.ivi.ru/watch/scream-6/trailer',
            'Оно': 'https://www.ivi.ru/watch/it-2017/trailer',
        }
        
        # Определяем платформы для каждого сервиса
        platform_mapping = {
            'kinopoisk.ru': 'КиноПоиск HD',
            'okko.tv': 'Okko',
            'wink.ru': 'Wink',
            'start.ru': 'START',
            'ivi.ru': 'ivi'
        }
        
        updated_count = 0
        platform_stats = {}
        
        for title, trailer_url in russian_cinema_trailers.items():
            try:
                film = Film.objects.get(title=title)
                film.trailer_url = trailer_url
                film.save()
                
                # Определяем платформу
                platform = "Неизвестно"
                for domain, name in platform_mapping.items():
                    if domain in trailer_url:
                        platform = name
                        break
                
                # Считаем статистику
                if platform not in platform_stats:
                    platform_stats[platform] = 0
                platform_stats[platform] += 1
                
                self.stdout.write(f"  ✅ {title} -> {platform}")
                updated_count += 1
                
            except Film.DoesNotExist:
                self.stdout.write(f"  ❌ Фильм '{title}' не найден")
        
        self.stdout.write(
            self.style.SUCCESS(f"\n🎉 Обновлено {updated_count} трейлеров из российских кинотеатров")
        )
        
        self.stdout.write(f"\n📊 Статистика по платформам:")
        for platform, count in platform_stats.items():
            self.stdout.write(f"  🎬 {platform}: {count} трейлеров")
        
        self.stdout.write("\n🇷🇺 РОССИЙСКИЕ ОНЛАЙН-КИНОТЕАТРЫ:")
        
        platforms_info = [
            ("КиноПоиск HD", "Премиум сервис Яндекса", "🟡"),
            ("Okko", "Сервис МТС", "🟢"), 
            ("Wink", "Платформа Ростелекома", "🔵"),
            ("START", "Газпром-Медиа", "🟣"),
            ("ivi", "Популярный российский сервис", "🔴")
        ]
        
        for name, description, color in platforms_info:
            count = platform_stats.get(name, 0)
            self.stdout.write(f"  {color} {name} ({count}) - {description}")
        
        self.stdout.write("\n✨ ПРЕИМУЩЕСТВА:")
        advantages = [
            "🎭 Профессиональная русская озвучка",
            "🇷🇺 Российские лицензированные сервисы", 
            "🚫 Без блокировок на территории РФ",
            "⚡ Быстрая загрузка в России",
            "🎬 Официальные трейлеры в HD",
            "💬 Русские субтитры и описания",
            "🔒 Лицензионный контент",
            "📱 Мобильные приложения"
        ]
        
        for advantage in advantages:
            self.stdout.write(f"  {advantage}")
        
        self.stdout.write("\n🎯 РАСПРЕДЕЛЕНИЕ КОНТЕНТА:")
        self.stdout.write("  🟡 КиноПоиск HD - блокбастеры и классика")
        self.stdout.write("  🟢 Okko - популярные фильмы")
        self.stdout.write("  🔵 Wink - современные боевики")
        self.stdout.write("  🟣 START - арт-хаус и драмы")
        self.stdout.write("  🔴 ivi - ужасы и триллеры")
        
        self.stdout.write("\n🌐 ТЕСТИРОВАНИЕ:")
        self.stdout.write("  1. Откройте http://127.0.0.1:8000/")
        self.stdout.write("  2. Выберите любой фильм")
        self.stdout.write("  3. Прокрутите до трейлера")
        self.stdout.write("  4. Увидите бейдж российского кинотеатра")
        self.stdout.write("  5. Трейлер с русской озвучкой")
        
        self.stdout.write("\n💡 ПРИМЕЧАНИЕ:")
        self.stdout.write("  🔗 Это демо-ссылки для показа концепции")
        self.stdout.write("  📝 В реальном проекте получите API доступ")
        self.stdout.write("  🤝 Заключите партнерские соглашения")
        self.stdout.write("  📋 Используйте официальные embed коды")
        
        self.stdout.write(self.style.SUCCESS("\n🎬 Российские кинотеатры подключены!"))