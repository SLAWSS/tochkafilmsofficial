from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Создает демо-трейлеры с YouTube для тестирования'

    def handle(self, *args, **options):
        self.stdout.write("🎬 Создание демо-трейлеров...")
        
        # Используем реальные YouTube трейлеры для демонстрации
        # (в реальном проекте замените на VK Video и Rutube)
        demo_trailers = {
            'Начало': 'https://www.youtube.com/embed/YoHD9XEInc0',
            'Интерстеллар': 'https://www.youtube.com/embed/zSWdZVtXT7E',
            'Темный рыцарь': 'https://www.youtube.com/embed/EXeTwQWrcwY',
            'Побег из Шоушенка': 'https://www.youtube.com/embed/6hB3S9bIaco',
            'Форрест Гамп': 'https://www.youtube.com/embed/bLvqoHBptjg',
            'Матрица': 'https://www.youtube.com/embed/vKQi3bIA1HI',
            'Криминальное чтиво': 'https://www.youtube.com/embed/s7EdQ4FqbhY',
            'Бойцовский клуб': 'https://www.youtube.com/embed/qtRKdVHc-cE',
            'Крик': 'https://www.youtube.com/embed/AWm_mkbdpCA',
            'Крик 2': 'https://www.youtube.com/embed/t8Rqy8p_HrE',
            'Крик 3': 'https://www.youtube.com/embed/RqGF4WoDKNQ',
            'Крик 4': 'https://www.youtube.com/embed/g_akRMqsaKc',
            'Крик 5': 'https://www.youtube.com/embed/beToTslH17s',
            'Крик 6': 'https://www.youtube.com/embed/h74AXqw4Opc',
            'Оно': 'https://www.youtube.com/embed/FnCdOQsX5kc',
            'Джон Уик': 'https://www.youtube.com/embed/C0BMx-qxsP4',
            'Мстители: Финал': 'https://www.youtube.com/embed/TcMBFSGVi1c',
            'Джокер': 'https://www.youtube.com/embed/zAGVQLHvwOY',
            'Паразиты': 'https://www.youtube.com/embed/5xH0HfJHsaY',
            'Дюна': 'https://www.youtube.com/embed/n9xhJrPXop4',
        }
        
        updated_count = 0
        
        for title, trailer_url in demo_trailers.items():
            try:
                film = Film.objects.get(title=title)
                film.trailer_url = trailer_url
                film.save()
                
                self.stdout.write(f"  ✅ {title} -> YouTube (демо)")
                updated_count += 1
                
            except Film.DoesNotExist:
                self.stdout.write(f"  ❌ Фильм '{title}' не найден")
        
        self.stdout.write(
            self.style.SUCCESS(f"\n🎉 Обновлено {updated_count} демо-трейлеров")
        )
        
        self.stdout.write("\n📺 ДЕМО-ТРЕЙЛЕРЫ УСТАНОВЛЕНЫ!")
        self.stdout.write("   Используются YouTube embed для демонстрации")
        self.stdout.write("   В продакшене замените на VK Video и Rutube")
        
        self.stdout.write("\n🌐 ТЕСТИРОВАНИЕ:")
        self.stdout.write("  1. Откройте любой фильм")
        self.stdout.write("  2. Прокрутите до секции 'Трейлер'")
        self.stdout.write("  3. Проверьте воспроизведение")
        
        self.stdout.write("\n💡 ПРИМЕЧАНИЕ:")
        self.stdout.write("  🎬 Трейлеры теперь должны работать")
        self.stdout.write("  📱 Адаптивный дизайн")
        self.stdout.write("  ✨ Красивые анимации")
        self.stdout.write("  🎨 Платформенные бейджи")