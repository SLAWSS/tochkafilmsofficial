from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Проверяет русские трейлеры с VK Video и Rutube'

    def handle(self, *args, **kwargs):
        films = Film.objects.all()
        
        self.stdout.write(f'Проверка русских трейлеров для {films.count()} фильмов...\n')
        
        vk_films = []
        rutube_films = []
        no_trailer_films = []
        
        for film in films:
            if film.trailer_url:
                if 'vk.com' in film.trailer_url:
                    vk_films.append(film)
                    self.stdout.write(
                        self.style.SUCCESS(f'🇷🇺 VK Video: {film.title} ({film.year})')
                    )
                elif 'rutube.ru' in film.trailer_url:
                    rutube_films.append(film)
                    self.stdout.write(
                        self.style.SUCCESS(f'🇷🇺 Rutube: {film.title} ({film.year})')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Другая платформа: {film.title} - {film.trailer_url}')
                    )
            else:
                no_trailer_films.append(film)
                self.stdout.write(
                    self.style.ERROR(f'✗ Без трейлера: {film.title} ({film.year})')
                )
        
        self.stdout.write(f'\n📊 Статистика русских трейлеров:')
        self.stdout.write(f'Всего фильмов: {films.count()}')
        self.stdout.write(f'VK Video: {len(vk_films)} трейлеров')
        self.stdout.write(f'Rutube: {len(rutube_films)} трейлеров')
        self.stdout.write(f'Без трейлеров: {len(no_trailer_films)}')
        
        self.stdout.write(f'\n🎬 Распределение по жанрам:')
        
        # VK Video фильмы (ужасы и триллеры)
        if vk_films:
            self.stdout.write(f'VK Video (ужасы/триллеры):')
            for film in vk_films:
                categories = ', '.join([cat.name for cat in film.categories.all()])
                self.stdout.write(f'  • {film.title} - {categories}')
        
        # Rutube фильмы (драмы и фантастика)
        if rutube_films:
            self.stdout.write(f'\nRutube (драмы/фантастика/боевики):')
            for film in rutube_films:
                categories = ', '.join([cat.name for cat in film.categories.all()])
                self.stdout.write(f'  • {film.title} - {categories}')
        
        if len(vk_films) + len(rutube_films) == films.count():
            self.stdout.write(self.style.SUCCESS('\n🎉 У всех фильмов есть русские трейлеры!'))