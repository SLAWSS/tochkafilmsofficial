from django.core.management.base import BaseCommand
from films.models import Film
from django.db.models import Q


class Command(BaseCommand):
    help = 'Тестирует функцию поиска'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Тестирование поиска...")
        
        # Список тестовых запросов
        test_queries = [
            "крик",
            "Крик",
            "КРИК", 
            "матрица",
            "Матрица",
            "джокер",
            "боевик",
            "ужасы",
            "2023",
            "1999",
            "побег",
            "темный",
            "начало",
            "дюна"
        ]
        
        self.stdout.write("\n📋 Доступные фильмы:")
        for film in Film.objects.all().order_by('title'):
            categories = ", ".join([cat.name for cat in film.categories.all()])
            self.stdout.write(f"  • {film.title} ({film.year}) - {categories}")
        
        self.stdout.write(f"\n🧪 Тестирование {len(test_queries)} запросов:")
        
        for query in test_queries:
            # Имитируем точную логику поиска из views.py
            query_lower = query.lower()
            
            # Получаем все фильмы и фильтруем их в Python
            all_films = Film.objects.all().prefetch_related('categories')
            matching_films = []
            
            for film in all_films:
                # Проверяем название фильма
                if query_lower in film.title.lower():
                    matching_films.append(film.id)
                    continue
                    
                # Проверяем описание
                if query_lower in film.description.lower():
                    matching_films.append(film.id)
                    continue
                    
                # Проверяем категории
                for category in film.categories.all():
                    if query_lower in category.name.lower():
                        matching_films.append(film.id)
                        break
                
                # Проверяем год
                if query.isdigit() and query in str(film.year):
                    matching_films.append(film.id)
                    continue
            
            # Если найдены совпадения, получаем фильмы из базы
            films = []
            if matching_films:
                films = Film.objects.filter(id__in=matching_films).distinct()
            
            # Если ничего не найдено, попробуем поиск по частям слов
            if not matching_films and len(query) > 2:
                words = query_lower.split()
                for word in words:
                    if len(word) > 1:
                        for film in all_films:
                            if (word in film.title.lower() or 
                                word in film.description.lower() or
                                any(word in cat.name.lower() for cat in film.categories.all())):
                                matching_films.append(film.id)
                
                if matching_films:
                    films = Film.objects.filter(id__in=matching_films).distinct()
            
            count = len(matching_films)
            status = "✅" if count > 0 else "❌"
            
            self.stdout.write(f"  {status} '{query}' -> {count} результат(ов)")
            if count > 0 and count <= 3 and films:
                for film in films[:3]:
                    self.stdout.write(f"      - {film.title}")
        
        self.stdout.write(self.style.SUCCESS("\n✅ Тестирование завершено!"))
        self.stdout.write("\n💡 Для тестирования в браузере:")
        self.stdout.write("  http://127.0.0.1:8000/search/?q=крик")
        self.stdout.write("  http://127.0.0.1:8000/search/?q=боевик")
        self.stdout.write("  http://127.0.0.1:8000/search/?q=2023")