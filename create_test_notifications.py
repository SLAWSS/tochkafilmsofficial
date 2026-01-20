from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from films.models import Film, Notification


class Command(BaseCommand):
    help = 'Создает тестовые уведомления для пользователей'

    def handle(self, *args, **options):
        self.stdout.write("🔔 Создание тестовых уведомлений...")
        
        # Получаем всех пользователей
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.WARNING("Нет пользователей в системе"))
            return
        
        # Получаем несколько фильмов
        films = Film.objects.all()[:5]
        if not films.exists():
            self.stdout.write(self.style.WARNING("Нет фильмов в системе"))
            return
        
        notifications_created = 0
        
        for user in users:
            # Создаем уведомления разных типов
            
            # Уведомление о новом фильме
            if films:
                film = films[0]
                notification, created = Notification.objects.get_or_create(
                    user=user,
                    type='new_film',
                    title='Новый фильм добавлен!',
                    message=f'Добавлен новый фильм "{film.title}" ({film.year}). Не пропустите!',
                    film=film,
                    defaults={'is_read': False}
                )
                if created:
                    notifications_created += 1
            
            # Уведомление о рекомендации
            if len(films) > 1:
                film = films[1]
                notification, created = Notification.objects.get_or_create(
                    user=user,
                    type='recommendation',
                    title='Рекомендация для вас',
                    message=f'Основываясь на ваших предпочтениях, рекомендуем посмотреть "{film.title}"',
                    film=film,
                    defaults={'is_read': False}
                )
                if created:
                    notifications_created += 1
            
            # Уведомление о новом отзыве
            if len(films) > 2:
                film = films[2]
                notification, created = Notification.objects.get_or_create(
                    user=user,
                    type='new_review',
                    title='Новый отзыв',
                    message=f'Пользователи оставили новые отзывы на фильм "{film.title}"',
                    film=film,
                    defaults={'is_read': True}  # Этот отзыв уже прочитан
                )
                if created:
                    notifications_created += 1
        
        self.stdout.write(
            self.style.SUCCESS(f"✅ Создано {notifications_created} тестовых уведомлений")
        )
        
        # Показываем статистику
        total_notifications = Notification.objects.count()
        unread_notifications = Notification.objects.filter(is_read=False).count()
        
        self.stdout.write(f"📊 Всего уведомлений: {total_notifications}")
        self.stdout.write(f"📊 Непрочитанных: {unread_notifications}")