from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from films.models import Film, Notification
import random


class Command(BaseCommand):
    help = 'Создает тестовые уведомления'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        films = Film.objects.all()
        
        if not users.exists():
            self.stdout.write(self.style.ERROR('Нет пользователей для создания уведомлений'))
            return
        
        if not films.exists():
            self.stdout.write(self.style.ERROR('Нет фильмов для создания уведомлений'))
            return
        
        notifications_data = [
            {
                'type': 'new_film',
                'title': 'Новый фильм добавлен!',
                'message': 'На сайте появился новый фильм "{}" - не пропустите!',
            },
            {
                'type': 'recommendation',
                'title': 'Рекомендация для вас',
                'message': 'Основываясь на ваших предпочтениях, рекомендуем посмотреть "{}"',
            },
            {
                'type': 'new_review',
                'title': 'Новый отзыв',
                'message': 'Пользователи оставили новые отзывы о фильме "{}"',
            },
        ]
        
        created_count = 0
        for user in users:
            # Создаем 2-3 уведомления для каждого пользователя
            for _ in range(random.randint(2, 3)):
                notification_template = random.choice(notifications_data)
                film = random.choice(films)
                
                notification = Notification.objects.create(
                    user=user,
                    type=notification_template['type'],
                    title=notification_template['title'],
                    message=notification_template['message'].format(film.title),
                    film=film,
                    is_read=random.choice([True, False])  # Случайно помечаем как прочитанные
                )
                created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Создано {created_count} тестовых уведомлений')
        )