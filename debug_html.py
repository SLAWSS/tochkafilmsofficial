import requests
from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Проверяет HTML-код главной страницы'

    def handle(self, *args, **kwargs):
        try:
            response = requests.get("http://127.0.0.1:8000", timeout=5)
            if response.status_code == 200:
                html = response.text
                
                # Ищем теги img в HTML
                import re
                img_tags = re.findall(r'<img[^>]*src="([^"]*)"[^>]*>', html)
                
                self.stdout.write(f'Найдено {len(img_tags)} изображений в HTML:')
                for i, src in enumerate(img_tags, 1):
                    self.stdout.write(f'{i}. {src}')
                
                # Проверяем, есть ли постеры в HTML
                poster_count = len([src for src in img_tags if 'posters/' in src])
                self.stdout.write(f'\nПостеров найдено: {poster_count}')
                
                # Проверяем фильмы в базе
                films_with_posters = Film.objects.exclude(poster='').count()
                self.stdout.write(f'Фильмов с постерами в БД: {films_with_posters}')
                
                # Показываем часть HTML с фильмами
                if 'film-card' in html:
                    self.stdout.write('\n✓ Карточки фильмов найдены в HTML')
                else:
                    self.stdout.write('\n✗ Карточки фильмов НЕ найдены в HTML')
                
            else:
                self.stdout.write(self.style.ERROR(f'Ошибка HTTP: {response.status_code}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))
            self.stdout.write('Убедитесь, что сервер запущен: python manage.py runserver')