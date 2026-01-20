from django.core.management.base import BaseCommand
from films.models import Film, Category
from django.db import models


class Command(BaseCommand):
    help = 'Показывает статистику по категориям фильмов'

    def handle(self, *args, **options):
        self.show_categories_statistics()

    def show_categories_statistics(self):
        """Показывает детальную статистику по категориям"""
        categories = Category.objects.all()
        films = Film.objects.all()
        
        self.stdout.write("=" * 60)
        self.stdout.write("🎬 СТАТИСТИКА ПО КАТЕГОРИЯМ ФИЛЬМОВ")
        self.stdout.write("=" * 60)
        
        # Основная статистика
        self.stdout.write(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
        self.stdout.write(f"  Всего фильмов: {films.count()}")
        self.stdout.write(f"  Всего категорий: {categories.count()}")
        
        # Фильмы с категориями и без
        films_with_categories = films.filter(categories__isnull=False).distinct()
        films_without_categories = films.filter(categories__isnull=True)
        
        self.stdout.write(f"  Фильмов с категориями: {films_with_categories.count()}")
        self.stdout.write(f"  Фильмов без категорий: {films_without_categories.count()}")
        
        if categories.exists():
            # Статистика по категориям
            self.stdout.write(f"\n📋 СТАТИСТИКА ПО КАТЕГОРИЯМ:")
            
            categories_with_stats = categories.annotate(
                films_count=models.Count('films')
            ).order_by('-films_count')
            
            for category in categories_with_stats:
                films_count = category.films_count
                percentage = (films_count / films.count() * 100) if films.count() > 0 else 0
                
                self.stdout.write(f"  📁 {category.name}: {films_count} фильм{self.pluralize_films(films_count)} ({percentage:.1f}%)")
                
                # Показываем примеры фильмов
                example_films = category.films.all()[:3]
                if example_films:
                    films_list = ", ".join([f.title for f in example_films])
                    if films_count > 3:
                        films_list += f" и еще {films_count - 3}"
                    self.stdout.write(f"    Примеры: {films_list}")
            
            # Топ категории
            self.stdout.write(f"\n🏆 ТОП-5 КАТЕГОРИЙ:")
            top_categories = categories_with_stats[:5]
            for i, category in enumerate(top_categories, 1):
                self.stdout.write(f"  {i}. {category.name} - {category.films_count} фильм{self.pluralize_films(category.films_count)}")
        
        # Фильмы без категорий
        if films_without_categories.exists():
            self.stdout.write(f"\n⚠️  ФИЛЬМЫ БЕЗ КАТЕГОРИЙ ({films_without_categories.count()}):")
            for film in films_without_categories[:10]:
                self.stdout.write(f"  • {film.title} ({film.year})")
            
            if films_without_categories.count() > 10:
                self.stdout.write(f"  ... и еще {films_without_categories.count() - 10} фильмов")
        
        # Анализ по годам для семейных фильмов
        if categories.filter(name="Семейные").exists():
            family_category = categories.get(name="Семейные")
            self.stdout.write(f"\n👨‍👩‍👧‍👦 АНАЛИЗ СЕМЕЙНЫХ ФИЛЬМОВ:")
            
            family_films = family_category.films.all()
            if family_films:
                # По годам
                years = [film.year for film in family_films]
                if years:
                    avg_year = sum(years) / len(years)
                    min_year = min(years)
                    max_year = max(years)
                    
                    self.stdout.write(f"  📅 Средний год выпуска: {avg_year:.0f}")
                    self.stdout.write(f"  📅 Самый старый: {min_year}")
                    self.stdout.write(f"  📅 Самый новый: {max_year}")
                
                # По рейтингу
                ratings = [float(film.rating) for film in family_films]
                if ratings:
                    avg_rating = sum(ratings) / len(ratings)
                    max_rating = max(ratings)
                    min_rating = min(ratings)
                    
                    self.stdout.write(f"  ⭐ Средний рейтинг: {avg_rating:.1f}")
                    self.stdout.write(f"  ⭐ Лучший рейтинг: {max_rating}")
                    self.stdout.write(f"  ⭐ Худший рейтинг: {min_rating}")
                
                # Топ семейных фильмов
                top_family = family_films.order_by('-rating')[:5]
                self.stdout.write(f"  🏆 Топ-5 семейных фильмов:")
                for i, film in enumerate(top_family, 1):
                    self.stdout.write(f"    {i}. {film.title} ({film.year}) - ⭐ {film.rating}")
        
        # Рекомендации
        self.stdout.write(f"\n💡 РЕКОМЕНДАЦИИ:")
        
        if films_without_categories.exists():
            self.stdout.write(f"  ⚠️  Добавить категории к {films_without_categories.count()} фильмам")
        
        if categories.count() < 10:
            self.stdout.write(f"  📈 Создать больше категорий (сейчас {categories.count()})")
            self.stdout.write(f"     Предложения: Комедии, Драмы, Боевики, Фантастика, Мелодрамы")
        
        empty_categories = categories.filter(films__isnull=True)
        if empty_categories.exists():
            self.stdout.write(f"  🗑️  Удалить {empty_categories.count()} пустых категорий")
        
        if films_with_categories.count() == films.count():
            self.stdout.write(f"  ✅ Отлично! Все фильмы имеют категории")
        
        self.stdout.write(f"\n📋 ПОЛЕЗНЫЕ КОМАНДЫ:")
        self.stdout.write(f"  • Добавить семейные фильмы: python manage.py add_family_films")
        self.stdout.write(f"  • Посмотреть категории: /category/")
        self.stdout.write(f"  • Фильтр по категориям: /filter/")

    def pluralize_films(self, count):
        """Склонение слова 'фильм'"""
        if count % 10 == 1 and count % 100 != 11:
            return ""
        elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
            return "а"
        else:
            return "ов"