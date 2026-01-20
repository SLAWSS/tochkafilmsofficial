from django.core.management.base import BaseCommand
from films.models import Film
import os
from django.conf import settings
from django.core.files import File
import requests
from urllib.parse import urlparse


class Command(BaseCommand):
    help = 'Добавляет постеры к фильмам'

    def add_arguments(self, parser):
        parser.add_argument('--film-id', type=int, help='ID конкретного фильма')
        parser.add_argument('--poster-url', type=str, help='URL постера')
        parser.add_argument('--poster-file', type=str, help='Путь к файлу постера')

    def handle(self, *args, **options):
        if options['film_id']:
            try:
                film = Film.objects.get(id=options['film_id'])
                
                if options['poster_url']:
                    self.add_poster_from_url(film, options['poster_url'])
                elif options['poster_file']:
                    self.add_poster_from_file(film, options['poster_file'])
                else:
                    self.stdout.write("Укажите --poster-url или --poster-file")
                    
            except Film.DoesNotExist:
                self.stdout.write(f"Фильм с ID {options['film_id']} не найден")
        else:
            self.stdout.write("Укажите --film-id")

    def add_poster_from_url(self, film, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Получаем имя файла из URL
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)
                if not filename:
                    filename = f"{film.title.lower().replace(' ', '_')}_poster.jpg"
                
                # Сохраняем файл
                temp_file = f"/tmp/{filename}"
                with open(temp_file, 'wb') as f:
                    f.write(response.content)
                
                # Добавляем к фильму
                with open(temp_file, 'rb') as f:
                    film.poster.save(filename, File(f))
                
                os.remove(temp_file)
                self.stdout.write(f"Постер добавлен к фильму '{film.title}'")
            else:
                self.stdout.write(f"Ошибка загрузки: {response.status_code}")
        except Exception as e:
            self.stdout.write(f"Ошибка: {e}")

    def add_poster_from_file(self, film, file_path):
        try:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    filename = os.path.basename(file_path)
                    film.poster.save(filename, File(f))
                self.stdout.write(f"Постер добавлен к фильму '{film.title}'")
            else:
                self.stdout.write(f"Файл {file_path} не найден")
        except Exception as e:
            self.stdout.write(f"Ошибка: {e}")