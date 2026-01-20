import requests
from django.core.management.base import BaseCommand
from films.models import Film
from django.conf import settings


class Command(BaseCommand):
    help = 'Тестирует доступность медиа-файлов'

    def handle(self, *args, **kwargs):
        base_url = "http://127.0.0.1:8000"
        
        # Проверяем главную страницу
        try:
            response = requests.get(base_url, timeout=5)
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS(f'✓ Главная страница доступна: {response.status_code}'))
            else:
                self.stdout.write(self.style.ERROR(f'✗ Главная страница недоступна: {response.status_code}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Ошибка подключения к серверу: {e}'))
            return
        
        # Проверяем медиа-файлы
        films = Film.objects.all()[:3]  # Проверим первые 3 фильма
        
        for film in films:
            if film.poster:
                media_url = f"{base_url}{settings.MEDIA_URL}{film.poster.name}"
                try:
                    response = requests.get(media_url, timeout=5)
                    if response.status_code == 200:
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ {film.title}: {media_url} - доступен')
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR(f'✗ {film.title}: {media_url} - {response.status_code}')
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'✗ {film.title}: {media_url} - ошибка: {e}')
                    )
        
        # Проверяем статические файлы
        static_files = [
            'css/style.css',
            'images/logo.png',
            'images/action-icon.png'
        ]
        
        for static_file in static_files:
            static_url = f"{base_url}{settings.STATIC_URL}{static_file}"
            try:
                response = requests.get(static_url, timeout=5)
                if response.status_code == 200:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Статический файл: {static_url} - доступен')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Статический файл: {static_url} - {response.status_code}')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Статический файл: {static_url} - ошибка: {e}')
                )