from django.core.management.base import BaseCommand
from films.models import Actor, Film
from django.db import models


class Command(BaseCommand):
    help = 'Показывает статистику по актерам'

    def handle(self, *args, **options):
        self.show_actors_statistics()

    def show_actors_statistics(self):
        """Показывает детальную статистику по актерам"""
        actors = Actor.objects.all()
        films = Film.objects.all()
        
        self.stdout.write("=" * 50)
        self.stdout.write("🎭 СТАТИСТИКА АКТЕРОВ")
        self.stdout.write("=" * 50)
        
        # Основная статистика
        self.stdout.write(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
        self.stdout.write(f"  Всего актеров: {actors.count()}")
        self.stdout.write(f"  Всего фильмов: {films.count()}")
        
        # Актеры с фильмами
        actors_with_films = actors.filter(films__isnull=False).distinct()
        actors_without_films = actors.filter(films__isnull=True)
        
        self.stdout.write(f"  Актеров с фильмами: {actors_with_films.count()}")
        self.stdout.write(f"  Актеров без фильмов: {actors_without_films.count()}")
        
        # Фильмы с актерами
        films_with_actors = films.filter(actors__isnull=False).distinct()
        films_without_actors = films.filter(actors__isnull=True)
        
        self.stdout.write(f"  Фильмов с актерами: {films_with_actors.count()}")
        self.stdout.write(f"  Фильмов без актеров: {films_without_actors.count()}")
        
        if actors.exists():
            # Топ актеров по количеству фильмов
            self.stdout.write(f"\n🏆 ТОП АКТЕРОВ ПО ФИЛЬМАМ:")
            top_actors = actors.annotate(
                films_count=models.Count('films')
            ).order_by('-films_count')[:10]
            
            for i, actor in enumerate(top_actors, 1):
                films_count = actor.films_count
                if films_count > 0:
                    self.stdout.write(f"  {i}. {actor.name}: {films_count} фильм{self.pluralize_films(films_count)}")
            
            # Информация о возрасте актеров
            self.stdout.write(f"\n👥 ВОЗРАСТНАЯ СТАТИСТИКА:")
            ages = [actor.age for actor in actors]
            if ages:
                avg_age = sum(ages) / len(ages)
                min_age = min(ages)
                max_age = max(ages)
                
                self.stdout.write(f"  Средний возраст: {avg_age:.1f} лет")
                self.stdout.write(f"  Самый молодой: {min_age} лет")
                self.stdout.write(f"  Самый старший: {max_age} лет")
            
            # Список всех актеров
            self.stdout.write(f"\n📋 СПИСОК ВСЕХ АКТЕРОВ:")
            for actor in actors.order_by('name'):
                films_count = actor.films.count()
                self.stdout.write(f"  • {actor.name} ({actor.age} лет) - {films_count} фильм{self.pluralize_films(films_count)}")
                
                # Показываем фильмы актера
                if films_count > 0:
                    films_list = ", ".join([film.title for film in actor.films.all()[:3]])
                    if films_count > 3:
                        films_list += f" и еще {films_count - 3}"
                    self.stdout.write(f"    Фильмы: {films_list}")
        
        # Фильмы без актеров
        if films_without_actors.exists():
            self.stdout.write(f"\n⚠️  ФИЛЬМЫ БЕЗ АКТЕРОВ ({films_without_actors.count()}):")
            for film in films_without_actors[:10]:
                self.stdout.write(f"  • {film.title} ({film.year})")
            
            if films_without_actors.count() > 10:
                self.stdout.write(f"  ... и еще {films_without_actors.count() - 10} фильмов")
        
        # Рекомендации
        self.stdout.write(f"\n💡 РЕКОМЕНДАЦИИ:")
        
        if actors_without_films.exists():
            self.stdout.write(f"  ⚠️  Связать {actors_without_films.count()} актеров с фильмами")
        
        if films_without_actors.exists():
            self.stdout.write(f"  ⚠️  Добавить актеров к {films_without_actors.count()} фильмам")
        
        if actors.count() < 20:
            self.stdout.write(f"  📈 Добавить больше актеров (сейчас {actors.count()})")
        
        if actors.count() > 0 and films_with_actors.count() == films.count():
            self.stdout.write(f"  ✅ Отлично! Все фильмы имеют актеров")
        
        self.stdout.write(f"\n📋 ПОЛЕЗНЫЕ КОМАНДЫ:")
        self.stdout.write(f"  • Добавить актеров: python manage.py add_actors")
        self.stdout.write(f"  • Посмотреть актеров: /actors/")

    def pluralize_films(self, count):
        """Склонение слова 'фильм'"""
        if count % 10 == 1 and count % 100 != 11:
            return ""
        elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
            return "а"
        else:
            return "ов"