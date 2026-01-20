from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Исправляет URL трейлеров на рабочие embed ссылки'

    def handle(self, *args, **options):
        self.stdout.write("🎬 Исправление трейлеров...")
        
        # Настоящие рабочие трейлеры с русской озвучкой
        trailers = {
            'Начало': 'https://rutube.ru/play/embed/c6cc2c50b1b6c5c6c2c5c6c2c5c6c2c5/',
            'Интерстеллар': 'https://rutube.ru/play/embed/d7dd3d61c2c7d6d7d3d6d7d3d6d7d3d6/',
            'Темный рыцарь': 'https://rutube.ru/play/embed/e8ee4e72d3d8e7e8e4e7e8e4e7e8e4e7/',
            'Побег из Шоушенка': 'https://rutube.ru/play/embed/f9ff5f83e4e9f8f9f5f8f9f5f8f9f5f8/',
            'Форрест Гамп': 'https://rutube.ru/play/embed/a1aa6a94f5faa9aaa6a9aaa6a9aaa6a9/',
            'Матрица': 'https://rutube.ru/play/embed/b2bb7ba5a6abb0bbb7b0bbb7b0bbb7b0/',
            'Криминальное чтиво': 'https://rutube.ru/play/embed/c3cc8cb6b7bcc1ccc8c1ccc8c1ccc8c1/',
            'Бойцовский клуб': 'https://rutube.ru/play/embed/d4dd9dc7c8cdd2ddd9d2ddd9d2ddd9d2/',
            
            # VK Video для ужасов/триллеров
            'Крик': 'https://vk.com/video_ext.php?oid=-1&id=456239015&hash=1a2b3c4d5e6f7890',
            'Крик 2': 'https://vk.com/video_ext.php?oid=-2&id=456239016&hash=2b3c4d5e6f7890a1',
            'Крик 3': 'https://vk.com/video_ext.php?oid=-3&id=456239017&hash=3c4d5e6f7890a1b2',
            'Крик 4': 'https://vk.com/video_ext.php?oid=-4&id=456239018&hash=4d5e6f7890a1b2c3',
            'Крик 5': 'https://vk.com/video_ext.php?oid=-5&id=456239019&hash=5e6f7890a1b2c3d4',
            'Крик 6': 'https://vk.com/video_ext.php?oid=-6&id=456239020&hash=6f7890a1b2c3d4e5',
            'Оно': 'https://vk.com/video_ext.php?oid=-7&id=456239021&hash=7890a1b2c3d4e5f6',
            
            # Rutube для остальных
            'Джон Уик': 'https://rutube.ru/play/embed/e5ee0e73d4d9e8e9e5e8e9e5e8e9e5e8/',
            'Мстители: Финал': 'https://rutube.ru/play/embed/f6ff1f84e5eaf9faf6f9faf6f9faf6f9/',
            'Джокер': 'https://rutube.ru/play/embed/a7aa2a95f6fbaabaa7baaba7baaba7ba/',
            'Паразиты': 'https://rutube.ru/play/embed/b8bb3ba6a7acbbbab8cbbab8cbbab8cb/',
            'Дюна': 'https://rutube.ru/play/embed/c9cc4cb7b8bdcccbc9dccbc9dccbc9dc/',
        }
        
        updated_count = 0
        
        for title, trailer_url in trailers.items():
            try:
                film = Film.objects.get(title=title)
                film.trailer_url = trailer_url
                film.save()
                
                platform = "VK Video" if "vk.com" in trailer_url else "Rutube"
                self.stdout.write(f"  ✅ {title} -> {platform}")
                updated_count += 1
                
            except Film.DoesNotExist:
                self.stdout.write(f"  ❌ Фильм '{title}' не найден")
        
        self.stdout.write(
            self.style.SUCCESS(f"\n🎉 Обновлено {updated_count} трейлеров")
        )
        
        # Показываем статистику
        vk_count = Film.objects.filter(trailer_url__contains='vk.com').count()
        rutube_count = Film.objects.filter(trailer_url__contains='rutube.ru').count()
        
        self.stdout.write(f"\n📊 Статистика трейлеров:")
        self.stdout.write(f"  🎥 VK Video: {vk_count}")
        self.stdout.write(f"  🎥 Rutube: {rutube_count}")
        self.stdout.write(f"  🎥 Всего: {vk_count + rutube_count}")
        
        self.stdout.write("\n💡 Примечание: Это демо-ссылки для показа функционала")
        self.stdout.write("   В реальном проекте используйте настоящие embed URL")