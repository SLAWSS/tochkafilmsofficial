from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Демонстрация трейлеров из российских онлайн-кинотеатров'

    def handle(self, *args, **options):
        self.stdout.write("🎬 TochkaFilms - Российские Онлайн-Кинотеатры")
        self.stdout.write("=" * 70)
        
        self.stdout.write(self.style.SUCCESS("\n🇷🇺 РОССИЙСКИЕ КИНОТЕАТРЫ ПОДКЛЮЧЕНЫ!"))
        
        # Статистика по платформам
        platforms = {
            'КиноПоиск HD': Film.objects.filter(trailer_url__contains='kinopoisk.ru').count(),
            'Okko': Film.objects.filter(trailer_url__contains='okko.tv').count(),
            'Wink': Film.objects.filter(trailer_url__contains='wink.ru').count(),
            'START': Film.objects.filter(trailer_url__contains='start.ru').count(),
            'ivi': Film.objects.filter(trailer_url__contains='ivi.ru').count(),
        }
        
        self.stdout.write(f"\n📊 СТАТИСТИКА ПО ПЛАТФОРМАМ:")
        total_trailers = 0
        for platform, count in platforms.items():
            if count > 0:
                emoji = {
                    'КиноПоиск HD': '🟡',
                    'Okko': '🟢', 
                    'Wink': '🔵',
                    'START': '🟣',
                    'ivi': '🔴'
                }.get(platform, '📺')
                
                self.stdout.write(f"  {emoji} {platform}: {count} трейлеров")
                total_trailers += count
        
        self.stdout.write(f"\n🎬 ВСЕГО ТРЕЙЛЕРОВ: {total_trailers}")
        
        self.stdout.write(f"\n🎭 ФИЛЬМЫ ПО ПЛАТФОРМАМ:")
        
        # КиноПоиск HD
        kinopoisk_films = Film.objects.filter(trailer_url__contains='kinopoisk.ru')
        if kinopoisk_films.exists():
            self.stdout.write(f"\n🟡 КИНОПОИСК HD ({kinopoisk_films.count()}):")
            for film in kinopoisk_films:
                self.stdout.write(f"  🎬 {film.title} ({film.year})")
        
        # Okko
        okko_films = Film.objects.filter(trailer_url__contains='okko.tv')
        if okko_films.exists():
            self.stdout.write(f"\n🟢 OKKO ({okko_films.count()}):")
            for film in okko_films:
                self.stdout.write(f"  🎬 {film.title} ({film.year})")
        
        # Wink
        wink_films = Film.objects.filter(trailer_url__contains='wink.ru')
        if wink_films.exists():
            self.stdout.write(f"\n🔵 WINK ({wink_films.count()}):")
            for film in wink_films:
                self.stdout.write(f"  🎬 {film.title} ({film.year})")
        
        # START
        start_films = Film.objects.filter(trailer_url__contains='start.ru')
        if start_films.exists():
            self.stdout.write(f"\n🟣 START ({start_films.count()}):")
            for film in start_films:
                self.stdout.write(f"  🎬 {film.title} ({film.year})")
        
        # ivi
        ivi_films = Film.objects.filter(trailer_url__contains='ivi.ru')
        if ivi_films.exists():
            self.stdout.write(f"\n🔴 IVI ({ivi_films.count()}):")
            for film in ivi_films:
                self.stdout.write(f"  🎬 {film.title} ({film.year})")
        
        self.stdout.write(f"\n🇷🇺 ПРЕИМУЩЕСТВА РОССИЙСКИХ КИНОТЕАТРОВ:")
        advantages = [
            "🎭 Профессиональная русская озвучка и дубляж",
            "🇷🇺 Лицензированные российские сервисы",
            "🚫 Без блокировок и ограничений в РФ",
            "⚡ Быстрая загрузка на территории России",
            "🎬 Официальные трейлеры в HD и 4K качестве",
            "💬 Русские субтитры и описания фильмов",
            "🔒 Лицензионный контент без пиратства",
            "📱 Мобильные приложения для всех устройств",
            "💳 Российские способы оплаты",
            "🎯 Персональные рекомендации на русском"
        ]
        
        for advantage in advantages:
            self.stdout.write(f"  {advantage}")
        
        self.stdout.write(f"\n🎨 НОВЫЙ ДИЗАЙН:")
        design_features = [
            "🟡 Желтые бейджи для КиноПоиск HD",
            "🟢 Зеленые бейджи для Okko", 
            "🔵 Синие бейджи для Wink",
            "🟣 Фиолетовые бейджи для START",
            "🔴 Красные бейджи для ivi",
            "✨ Анимации свечения для каждой платформы",
            "🌊 Плавные переходы и hover эффекты",
            "📱 Адаптивный дизайн для мобильных"
        ]
        
        for feature in design_features:
            self.stdout.write(f"  {feature}")
        
        self.stdout.write(f"\n🌐 ТЕСТИРОВАНИЕ:")
        test_recommendations = [
            ("Начало", "КиноПоиск HD", "Научная фантастика"),
            ("Форрест Гамп", "Okko", "Драма-комедия"),
            ("Джон Уик", "Wink", "Боевик"),
            ("Паразиты", "START", "Арт-хаус драма"),
            ("Крик", "ivi", "Ужасы")
        ]
        
        self.stdout.write("  Рекомендуемые фильмы для тестирования:")
        for title, platform, genre in test_recommendations:
            emoji = {
                'КиноПоиск HD': '🟡',
                'Okko': '🟢',
                'Wink': '🔵', 
                'START': '🟣',
                'ivi': '🔴'
            }.get(platform, '📺')
            
            self.stdout.write(f"  {emoji} {title} ({platform}) - {genre}")
        
        self.stdout.write(f"\n📋 ИНСТРУКЦИЯ:")
        steps = [
            "1. Откройте http://127.0.0.1:8000/",
            "2. Выберите любой фильм из списка",
            "3. Прокрутите до секции трейлера",
            "4. Увидите цветной бейдж российского кинотеатра",
            "5. Кликните для просмотра трейлера",
            "6. Наслаждайтесь русской озвучкой! 🇷🇺"
        ]
        
        for step in steps:
            self.stdout.write(f"  {step}")
        
        self.stdout.write(self.style.SUCCESS(f"\n🎉 ГОТОВО!"))
        self.stdout.write("🇷🇺 Теперь TochkaFilms использует только российские")
        self.stdout.write("📺 онлайн-кинотеатры с качественной русской озвучкой!")
        
        self.stdout.write(f"\n💡 В ПРОДАКШЕНЕ:")
        self.stdout.write("  🤝 Заключите партнерские соглашения")
        self.stdout.write("  📋 Получите официальные API ключи")
        self.stdout.write("  🔗 Используйте настоящие embed коды")
        self.stdout.write("  💰 Настройте монетизацию")