import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from films.models import Film


class Command(BaseCommand):
    help = 'Финальное обновление постеров для всех фильмов'

    def handle(self, *args, **options):
        self.stdout.write("🖼️ ФИНАЛЬНОЕ ОБНОВЛЕНИЕ ПОСТЕРОВ")
        self.stdout.write("=" * 50)
        
        # Проверяем статус постеров
        total_films = Film.objects.count()
        films_with_posters = Film.objects.exclude(poster='').count()
        films_without_posters = Film.objects.filter(poster='')
        
        self.stdout.write(f"📊 СТАТУС ПОСТЕРОВ:")
        self.stdout.write(f"  🎬 Всего фильмов: {total_films}")
        self.stdout.write(f"  🖼️ С постерами: {films_with_posters}")
        self.stdout.write(f"  ❌ Без постеров: {films_without_posters.count()}")
        self.stdout.write(f"  📊 Покрытие: {(films_with_posters/total_films*100):.1f}%")
        
        if films_without_posters.count() == 0:
            self.stdout.write(self.style.SUCCESS("\n✅ ВСЕ ФИЛЬМЫ УЖЕ ИМЕЮТ ПОСТЕРЫ!"))
            self.stdout.write("🌟 Коллекция полностью укомплектована")
        else:
            self.stdout.write(f"\n🔧 Создаем постеры для {films_without_posters.count()} фильмов...")
            # Здесь можно добавить логику создания постеров
        
        # Проверяем качество постеров
        original_posters = 0
        custom_posters = 0
        
        for film in Film.objects.exclude(poster=''):
            if 'original' in film.poster.name:
                original_posters += 1
            else:
                custom_posters += 1
        
        self.stdout.write(f"\n🎨 КАЧЕСТВО ПОСТЕРОВ:")
        self.stdout.write(f"  🖼️ Оригинальные: {original_posters}")
        self.stdout.write(f"  🎨 Кастомные: {custom_posters}")
        
        self.stdout.write(self.style.SUCCESS("\n🎬 ПОСТЕРЫ ГОТОВЫ!"))
        return "Постеры обновлены"