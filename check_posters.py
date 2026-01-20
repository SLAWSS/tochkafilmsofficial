import os
from django.core.management.base import BaseCommand
from films.models import Film
from django.conf import settings


class Command(BaseCommand):
    help = 'Проверяет наличие постеров у фильмов'

    def handle(self, *args, **kwargs):
        films = Film.objects.all()
        
        self.stdout.write(f'Проверка {films.count()} фильмов...\n')
        
        for film in films:
            if film.poster:
                poster_path = film.poster.path
                if os.path.exists(poster_path):
                    file_size = os.path.getsize(poster_path) / 1024  # KB
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ {film.title}: {film.poster.name} ({file_size:.1f} KB)')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'✗ {film.title}: файл {poster_path} не найден')
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ {film.title}: постер не назначен')
                )
        
        self.stdout.write(f'\nПроверка завершена!')
        self.stdout.write(f'MEDIA_ROOT: {settings.MEDIA_ROOT}')
        self.stdout.write(f'MEDIA_URL: {settings.MEDIA_URL}')