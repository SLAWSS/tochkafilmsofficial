import os
from PIL import Image
from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Проверяет информацию об изображениях'

    def handle(self, *args, **kwargs):
        films = Film.objects.all()
        
        self.stdout.write('Информация о постерах:\n')
        
        for film in films:
            if film.poster:
                poster_path = film.poster.path
                if os.path.exists(poster_path):
                    try:
                        # Открываем изображение
                        with Image.open(poster_path) as img:
                            width, height = img.size
                            format_name = img.format
                            mode = img.mode
                            
                        file_size = os.path.getsize(poster_path)
                        
                        self.stdout.write(
                            f'✓ {film.title}:\n'
                            f'  Файл: {film.poster.name}\n'
                            f'  Размер: {width}x{height} px\n'
                            f'  Формат: {format_name} ({mode})\n'
                            f'  Размер файла: {file_size} байт\n'
                            f'  URL: /media/{film.poster.name}\n'
                        )
                        
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'✗ {film.title}: Ошибка чтения изображения - {e}')
                        )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'✗ {film.title}: Файл не найден - {poster_path}')
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ {film.title}: Постер не назначен')
                )