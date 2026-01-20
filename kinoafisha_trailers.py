from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Добавляет трейлеры с КиноАфиши и других российских кино-сайтов'

    def handle(self, *args, **options):
        self.stdout.write("🎬 Добавление трейлеров с российских кино-сайтов...")
        
        # Трейлеры с российских кино-порталов и сайтов
        russian_movie_sites_trailers = {
         
            'Начало': 'https://rutube.ru/video/b8e3e1f388dfc3220b512ac166c09cac/?r=plwd',
            'Интерстеллар': 'https://rutube.ru/video/ff9ab42ec1558c84d684573c4688b792/?r=plwd',
            'Темный рыцарь': 'https://rutube.ru/video/56ede5a2638f358c4d5a154c7ed29bfc/?r=plwd',
            'Побег из Шоушенка': 'https://rutube.ru/video/b240375fefe352b526f127f89cb37b4c/?r=plwd',
            
           
            'Форрест Гамп': 'https://rutube.ru/video/c9b657dcd5bcd4c08513ee6833d3f524/?r=plwd',
            'Матрица': 'https://rutube.ru/video/b4875ee9b7bf0601927b4cf85d1a777c/?r=plwd',
            'Криминальное чтиво': 'https://rutube.ru/video/b65d802a457cbde62455c5d45ab1ad4b/?r=plwd',
            'Бойцовский клуб': 'https://rutube.ru/video/75c6c0dac432b321115215886676009e/?r=plwd',
            
           
            'Джон Уик': 'https://rutube.ru/video/896068b08376493192edb927d097608e/?r=plwd',
            'Мстители: Финал': 'https://rutube.ru/video/654239b83f9b68bb60f67ae73230f757/?r=plwd',
            'Джокер': 'https://rutube.ru/video/9b1d44b7e6af5df1cbc32fda32e17898/?r=plwd',
            
           
            'Паразиты': 'https://rutube.ru/video/f04be1bc4112cccc5251a7c8f3adfb27/?r=plwd',
            'Дюна': 'https://rutube.ru/video/8d44ef5abeeaa7089c94bb23bcde4135/?r=plwd',
            
            )
            'Крик': 'https://rutube.ru/video/e584d3c5870b670030c4683e79e7ef00/?r=plwd',
            'Крик 2': 'https://rutube.ru/video/aaef0d445de01ad595cafbb279af0978/?r=plwd',
            'Крик 3': 'https://hdrezka.ag/films/horror/1236-scream-3.html#trailer',
            'Крик 4': 'https://rutube.ru/video/b02b29d9c806e09ea6a5cac53e85b4e8/?r=plwd',
            'Крик 5': 'https://rutube.ru/video/1c671200addedcbb92807348543631ad/?r=plwd',
            'Крик 6': 'https://rutube.ru/video/3413296da063832aabd17a8d5fd2a0af/?r=plwd',
            'Оно': 'https://rutube.ru/video/bb6134a9de89a45082c655b85088bf70/?r=plwd',
        }
        
       
       
        }
        
        updated_count = 0
        platform_stats = {}
        
        for title, trailer_url in russian_movie_sites_trailers.items():
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
            self.style.SUCCESS(f"\n🎉 Обновлено {updated_count} трейлеров с российских кино-сайтов")
        )
        
        self.stdout.write(f"\n📊 Статистика по сайтам:")
        for platform, count in platform_stats.items():
            self.stdout.write(f"  🎬 {platform}: {count} трейлеров")
        
        self.stdout.write("\n🇷🇺 РОССИЙСКИЕ КИНО-САЙТЫ:")
        
        sites_info = [
            ("КиноАфиша", "Популярный российский кино-портал", "🎭"),
            ("Кино-Театр.ру", "Старейший российский кино-сайт", "🎪"), 
            ("Film.ru", "Современный кино-портал", "🎬"),
            ("Кинокрад", "Популярный стриминговый сайт", "🎯"),
            ("HDRezka", "Российская стриминговая платформа", "📺")
        ]
        
        for name, description, emoji in sites_info:
            count = platform_stats.get(name, 0)
            self.stdout.write(f"  {emoji} {name} ({count}) - {description}")
        
        self.stdout.write("\n✨ ПРЕИМУЩЕСТВА РОССИЙСКИХ КИНО-САЙТОВ:")
        advantages = [
            "🎭 Русские трейлеры с профессиональной озвучкой",
            "🇷🇺 Российские домены без блокировок", 
            "🚫 Доступность на территории РФ",
            "⚡ Быстрая загрузка для российских пользователей",
            "🎬 Качественные трейлеры и превью",
            "💬 Русские описания и рецензии",
            "🔒 Стабильная работа сервисов",
            "📱 Мобильная оптимизация",
            "🎯 Популярность среди российской аудитории",
            "📺 Интеграция с российскими стримингами"
        ]
        
        for advantage in advantages:
            self.stdout.write(f"  {advantage}")
        
        self.stdout.write("\n🎯 РАСПРЕДЕЛЕНИЕ КОНТЕНТА:")
        self.stdout.write("  🎭 КиноАфиша - блокбастеры и новинки")
        self.stdout.write("  🎪 Кино-Театр.ру - классика и артхаус")
        self.stdout.write("  🎬 Film.ru - современное кино")
        self.stdout.write("  🎯 Кинокрад - популярные фильмы")
        self.stdout.write("  📺 HDRezka - ужасы и триллеры")
        
        self.stdout.write("\n🌐 ТЕСТИРОВАНИЕ:")
        self.stdout.write("  1. Откройте http://127.0.0.1:8000/")
        self.stdout.write("  2. Выберите любой фильм")
        self.stdout.write("  3. Прокрутите до трейлера")
        self.stdout.write("  4. Увидите бейдж российского кино-сайта")
        self.stdout.write("  5. Кликните для перехода на сайт с трейлером")
        
        self.stdout.write("\n💡 ОСОБЕННОСТИ:")
        self.stdout.write("  🔗 Прямые ссылки на страницы с трейлерами")
        self.stdout.write("  📱 Мобильная совместимость")
        self.stdout.write("  🇷🇺 Русский интерфейс всех сайтов")
        self.stdout.write("  ⚡ Быстрый доступ к контенту")
        self.stdout.write("  🎬 Качественные трейлеры")
        
        self.stdout.write(self.style.SUCCESS("\n🎬 Российские кино-сайты подключены!"))