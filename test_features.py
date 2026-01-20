from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from films.models import Film, Category, ViewHistory, Notification


class Command(BaseCommand):
    help = 'Тестирует все новые функции сайта'

    def handle(self, *args, **options):
        self.stdout.write("🧪 Тестирование новых функций TochkaFilms...")
        
        # Проверяем модели
        self.stdout.write("\n📊 Статистика базы данных:")
        self.stdout.write(f"  Пользователи: {User.objects.count()}")
        self.stdout.write(f"  Фильмы: {Film.objects.count()}")
        self.stdout.write(f"  Категории: {Category.objects.count()}")
        self.stdout.write(f"  История просмотров: {ViewHistory.objects.count()}")
        self.stdout.write(f"  Уведомления: {Notification.objects.count()}")
        
        # Проверяем уведомления
        unread_notifications = Notification.objects.filter(is_read=False).count()
        self.stdout.write(f"  Непрочитанные уведомления: {unread_notifications}")
        
        # Проверяем топ фильмы
        top_films = Film.objects.order_by('-rating')[:5]
        self.stdout.write(f"\n🏆 Топ-5 фильмов по рейтингу:")
        for i, film in enumerate(top_films, 1):
            self.stdout.write(f"  {i}. {film.title} - ⭐ {film.rating}")
        
        # Проверяем категории
        self.stdout.write(f"\n📂 Категории:")
        for category in Category.objects.all():
            films_count = category.films.count()
            self.stdout.write(f"  {category.name}: {films_count} фильмов")
        
        # Проверяем трейлеры
        films_with_trailers = Film.objects.exclude(trailer_url='').count()
        self.stdout.write(f"\n🎬 Фильмы с трейлерами: {films_with_trailers}")
        
        # Проверяем русские трейлеры
        vk_trailers = Film.objects.filter(trailer_url__contains='vk.com').count()
        rutube_trailers = Film.objects.filter(trailer_url__contains='rutube.ru').count()
        self.stdout.write(f"  VK Video: {vk_trailers}")
        self.stdout.write(f"  Rutube: {rutube_trailers}")
        
        self.stdout.write(self.style.SUCCESS("\n✅ Тестирование завершено!"))
        
        # Рекомендации
        self.stdout.write("\n💡 Рекомендации:")
        if User.objects.count() == 0:
            self.stdout.write("  - Создайте суперпользователя: python manage.py createsuperuser")
        if unread_notifications == 0:
            self.stdout.write("  - Создайте тестовые уведомления: python manage.py create_test_notifications")
        
        self.stdout.write("\n🌐 Доступные страницы:")
        self.stdout.write("  - Главная: http://127.0.0.1:8000/")
        self.stdout.write("  - Топ фильмы: http://127.0.0.1:8000/top/")
        self.stdout.write("  - Фильтр: http://127.0.0.1:8000/filter/")
        self.stdout.write("  - История: http://127.0.0.1:8000/history/")
        self.stdout.write("  - Уведомления: http://127.0.0.1:8000/notifications/")
        self.stdout.write("  - Админка: http://127.0.0.1:8000/admin/")