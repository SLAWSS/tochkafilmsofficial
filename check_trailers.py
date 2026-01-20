from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Проверяет фильмы без трейлеров'

    def handle(self, *args, **options):
        films = Film.objects.all()
        
        self.stdout.write(f"Всего фильмов в базе: {films.count()}")
        self.stdout.write("\n=== ФИЛЬМЫ БЕЗ ТРЕЙЛЕРОВ ===")
        
        missing_trailers = []
        has_trailers = []
        
        for film in films:
            if not film.trailer_url:
                missing_trailers.append(film)
                self.stdout.write(f"❌ ID: {film.id} - {film.title} ({film.year})")
            else:
                has_trailers.append(film)
                self.stdout.write(f"✅ ID: {film.id} - {film.title} ({film.year}) - {film.trailer_url}")
        
        self.stdout.write(f"\nФильмов без трейлеров: {len(missing_trailers)}")
        self.stdout.write(f"Фильмов с трейлерами: {len(has_trailers)}")
        
        if missing_trailers:
            self.stdout.write("\n=== СПИСОК ДЛЯ ДОБАВЛЕНИЯ ТРЕЙЛЕРОВ ===")
            for film in missing_trailers[:20]:  # Показываем первые 20
                self.stdout.write(f"{film.id}: {film.title} ({film.year})")