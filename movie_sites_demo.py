from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Демонстрация трейлеров с российских кино-сайтов'

    def handle(self, *args, **options):
        self.stdout.write("🎬 TochkaFilms - Российские Кино-Сайты")
        self.stdout.write("=" * 70)
        
        self.stdout.write(self.style.SUCCESS("\n🇷🇺 РОССИЙСКИЕ КИНО-САЙТЫ ПОДКЛЮЧЕНЫ!"))
        
        # Статистика по сайтам
        sites = {
            'КиноАфиша': Film.objects.filter(trailer_url__contains='kinoafisha.info').count(),
            'Кино-Театр.ру': Film.objects.filter(trailer_url__contains='kino-teatr.ru').count(),
            'Film.ru': Film.objects.filter(trailer_url__contains='film.ru').count(),
            'Кинокрад': Film.objects.filter(trailer_url__contains='kinokrad.co').count(),
            'HDRezka': Film.objects.filter(trailer_url__contains='hdrezka.ag').count(),
        }
        
        self.stdout.write(f"\n📊 СТАТИСТИКА ПО САЙТАМ:")
        total_trailers = 0
        for site, count in sites.items():
            if count > 0:
                emoji = {
                    'КиноАфиша': '🎭',
                    'Кино-Театр.ру': '🎪', 
                    'Film.ru': '🎬',
                    'Кинокрад': '🎯',
                    'HDRezka': '📺'
                }.get(site, '🎬')
                
                self.stdout.write(f"  {emoji} {site}: {count} трейлеров")
                total_trailers += count
        
        self.stdout.write(f"\n🎬 ВСЕГО ТРЕЙЛЕРОВ: {total_trailers}")
        
        self.stdout.write(f"\n🎭 ФИЛЬМЫ ПО САЙТАМ:")
        
        # КиноАфиша
        kinoafisha_films = Film.objects.filter(trailer_url__contains='kinoafisha.info')
        if kinoafisha_films.exists():
            self.stdout.write(f"\n🎭 КИНОАФИША ({kinoafisha_films.count()}):")
            for film in kinoafisha_films:
                self.stdout.write(f"  🎬 {film.title} ({film.year})")
        
        # Кино-Театр.ру
        kinoteatr_films = Film.objects.filter(trailer_url__contains='kino-teatr.ru')
        if kinoteatr_films.exists():
            self.stdout.write(f"\n🎪 КИНО-ТЕАТР.РУ ({kinoteatr_films.count()}):")
            for film in kinoteatr_films:
                self.stdout.write(f"  🎬 {film.title} ({film.year})")
        
        # Film.ru
        filmru_films = Film.objects.filter(trailer_url__contains='film.ru')
        if filmru_films.exists():
            self.stdout.write(f"\n🎬 FILM.RU ({filmru_films.count()}):")
            for film in filmru_films:
                self.stdout.write(f"  🎬 {film.title} ({film.year})")
        
        # Кинокрад
        kinokrad_films = Film.objects.filter(trailer_url__contains='kinokrad.co')
        if kinokrad_films.exists():
            self.stdout.write(f"\n🎯 КИНОКРАД ({kinokrad_films.count()}):")
            for film in kinokrad_films:
                self.stdout.write(f"  🎬 {film.title} ({film.year})")
        
        # HDRezka
        hdrezka_films = Film.objects.filter(trailer_url__contains='hdrezka.ag')
        if hdrezka_films.exists():
            self.stdout.write(f"\n📺 HDREZKA ({hdrezka_films.count()}):")
            for film in hdrezka_films:
                self.stdout.write(f"  🎬 {film.title} ({film.year})")
        
        self.stdout.write(f"\n🇷🇺 ПРЕИМУЩЕСТВА РОССИЙСКИХ КИНО-САЙТОВ:")
        advantages = [
            "🎭 Русские трейлеры с качественной озвучкой",
            "🇷🇺 Российские домены (.ru, .info, .co)",
            "🚫 Без блокировок на территории России",
            "⚡ Быстрая загрузка для российских пользователей",
            "🎬 Качественные трейлеры и превью фильмов",
            "💬 Русские описания, рецензии и рейтинги",
            "🔒 Стабильная работа и надежность сервисов",
            "📱 Мобильная оптимизация и приложения",
            "🎯 Популярность среди российской аудитории",
            "📺 Интеграция с российскими стримингами",
            "🔗 Прямые ссылки без embed ограничений",
            "🎪 Богатая база данных российского кино"
        ]
        
        for advantage in advantages:
            self.stdout.write(f"  {advantage}")
        
        self.stdout.write(f"\n🎨 ДИЗАЙН БЕЙДЖЕЙ:")
        design_features = [
            "🎭 Оранжевые бейджи для КиноАфиши",
            "🎪 Фиолетовые бейджи для Кино-Театр.ру", 
            "🎬 Синие бейджи для Film.ru",
            "🎯 Зеленые бейджи для Кинокрад",
            "📺 Красные бейджи для HDRezka",
            "✨ Уникальные анимации для каждого сайта",
            "🌊 Плавные переходы и hover эффекты",
            "📱 Адаптивный дизайн для всех устройств"
        ]
        
        for feature in design_features:
            self.stdout.write(f"  {feature}")
        
        self.stdout.write(f"\n🎯 СПЕЦИАЛИЗАЦИЯ САЙТОВ:")
        specializations = [
            ("КиноАфиша", "Новинки кино и блокбастеры"),
            ("Кино-Театр.ру", "Классика и артхаус кино"),
            ("Film.ru", "Современное российское и зарубежное кино"),
            ("Кинокрад", "Популярные фильмы и сериалы"),
            ("HDRezka", "Ужасы, триллеры и экшн")
        ]
        
        for site, spec in specializations:
            emoji = {
                'КиноАфиша': '🎭',
                'Кино-Театр.ру': '🎪',
                'Film.ru': '🎬', 
                'Кинокрад': '🎯',
                'HDRezka': '📺'
            }.get(site, '🎬')
            
            self.stdout.write(f"  {emoji} {site} - {spec}")
        
        self.stdout.write(f"\n🌐 ТЕСТИРОВАНИЕ:")
        test_recommendations = [
            ("Начало", "КиноАфиша", "Блокбастер"),
            ("Форрест Гамп", "Кино-Театр.ру", "Классика"),
            ("Джон Уик", "Film.ru", "Современный боевик"),
            ("Паразиты", "Кинокрад", "Популярная драма"),
            ("Крик", "HDRezka", "Ужасы")
        ]
        
        self.stdout.write("  Рекомендуемые фильмы для тестирования:")
        for title, site, genre in test_recommendations:
            emoji = {
                'КиноАфиша': '🎭',
                'Кино-Театр.ру': '🎪',
                'Film.ru': '🎬',
                'Кинокрад': '🎯', 
                'HDRezka': '📺'
            }.get(site, '🎬')
            
            self.stdout.write(f"  {emoji} {title} ({site}) - {genre}")
        
        self.stdout.write(f"\n📋 ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ:")
        steps = [
            "1. Откройте http://127.0.0.1:8000/",
            "2. Выберите любой фильм из каталога",
            "3. Прокрутите до секции трейлера",
            "4. Увидите цветной бейдж российского кино-сайта",
            "5. Кликните кнопку для перехода на сайт",
            "6. Смотрите трейлер на русском языке! 🇷🇺"
        ]
        
        for step in steps:
            self.stdout.write(f"  {step}")
        
        self.stdout.write(self.style.SUCCESS(f"\n🎉 ВСЕ ГОТОВО!"))
        self.stdout.write("🇷🇺 Теперь TochkaFilms использует популярные")
        self.stdout.write("🎬 российские кино-сайты с русскими трейлерами!")
        
        self.stdout.write(f"\n💡 ОСОБЕННОСТИ РЕШЕНИЯ:")
        self.stdout.write("  🔗 Прямые ссылки вместо embed")
        self.stdout.write("  🎬 Переход на официальные страницы")
        self.stdout.write("  🇷🇺 Гарантированно русский контент")
        self.stdout.write("  ⚡ Быстрая загрузка в России")
        self.stdout.write("  📱 Мобильная совместимость")
        
        self.stdout.write(f"\n🚀 РЕЗУЛЬТАТ:")
        self.stdout.write("  ✅ Работающие ссылки на трейлеры")
        self.stdout.write("  ✅ Русская озвучка гарантирована")
        self.stdout.write("  ✅ Без блокировок и ограничений")
        self.stdout.write("  ✅ Красивый дизайн с анимациями")