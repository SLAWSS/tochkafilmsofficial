from django.core.management.base import BaseCommand
from films.models import Film, Category, Review
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Показывает статус проекта TochkaFilms'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🎬 Статус проекта TochkaFilms'))
        self.stdout.write('=' * 50)
        
        # Статистика фильмов
        total_films = Film.objects.count()
        films_with_posters = Film.objects.exclude(poster='').count()
        films_with_trailers = Film.objects.exclude(trailer_url='').count()
        featured_films = Film.objects.filter(is_featured=True).count()
        
        self.stdout.write(f'\n📊 Фильмы:')
        self.stdout.write(f'  Всего фильмов: {total_films}')
        self.stdout.write(f'  С постерами: {films_with_posters}')
        self.stdout.write(f'  С трейлерами: {films_with_trailers}')
        self.stdout.write(f'  Рекомендуемых: {featured_films}')
        
        # Статистика категорий
        total_categories = Category.objects.count()
        self.stdout.write(f'\n📁 Категории: {total_categories}')
        for category in Category.objects.all():
            films_count = category.films.count()
            self.stdout.write(f'  {category.name}: {films_count} фильмов')
        
        # Статистика пользователей
        total_users = User.objects.count()
        total_reviews = Review.objects.count()
        
        self.stdout.write(f'\n👥 Пользователи:')
        self.stdout.write(f'  Всего пользователей: {total_users}')
        self.stdout.write(f'  Всего отзывов: {total_reviews}')
        
        # Топ фильмов по рейтингу
        top_films = Film.objects.order_by('-rating')[:5]
        self.stdout.write(f'\n⭐ Топ-5 фильмов по рейтингу:')
        for i, film in enumerate(top_films, 1):
            self.stdout.write(f'  {i}. {film.title} ({film.year}) - ⭐ {film.rating}')
        
        # Проверка готовности
        self.stdout.write(f'\n✅ Проверка готовности:')
        
        checks = [
            (total_films > 0, f'Фильмы добавлены ({total_films})'),
            (films_with_posters == total_films, f'Все постеры созданы ({films_with_posters}/{total_films})'),
            (films_with_trailers == total_films, f'Все трейлеры добавлены ({films_with_trailers}/{total_films})'),
            (total_categories > 0, f'Категории созданы ({total_categories})'),
            (total_users > 0, f'Администратор создан ({total_users})'),
        ]
        
        all_ready = True
        for check_passed, message in checks:
            if check_passed:
                self.stdout.write(f'  ✓ {message}')
            else:
                self.stdout.write(f'  ✗ {message}')
                all_ready = False
        
        # Статистика русских трейлеров
        vk_trailers = Film.objects.filter(trailer_url__contains='vk.com').count()
        rutube_trailers = Film.objects.filter(trailer_url__contains='rutube.ru').count()
        
        self.stdout.write(f'\n🇷🇺 Русские трейлеры:')
        self.stdout.write(f'  VK Video: {vk_trailers} трейлеров')
        self.stdout.write(f'  Rutube: {rutube_trailers} трейлеров')
        
        self.stdout.write('\n' + '=' * 50)
        if all_ready:
            self.stdout.write(self.style.SUCCESS('🚀 Проект готов к запуску!'))
            self.stdout.write('🇷🇺 Все трейлеры с русской озвучкой!')
            self.stdout.write('Запустите: python manage.py runserver')
            self.stdout.write('Откройте: http://127.0.0.1:8000/')
        else:
            self.stdout.write(self.style.ERROR('⚠ Проект не готов. Выполните: python manage.py setup_project'))