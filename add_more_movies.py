from django.core.management.base import BaseCommand
from films.models import Category, Film


class Command(BaseCommand):
    help = 'Добавляет еще популярные фильмы'

    def handle(self, *args, **kwargs):
        # Получаем категории
        action_cat, _ = Category.objects.get_or_create(name="Боевик", defaults={"slug": "action"})
        comedy_cat, _ = Category.objects.get_or_create(name="Комедия", defaults={"slug": "comedy"})
        drama_cat, _ = Category.objects.get_or_create(name="Драма", defaults={"slug": "drama"})
        scifi_cat, _ = Category.objects.get_or_create(name="Фантастика", defaults={"slug": "sci-fi"})
        thriller_cat, _ = Category.objects.get_or_create(name="Триллер", defaults={"slug": "thriller"})
        horror_cat, _ = Category.objects.get_or_create(name="Ужасы", defaults={"slug": "horror"})

        # Дополнительные популярные фильмы
        additional_movies = [
            {
                'title': 'Джон Уик',
                'description': 'Легендарный киллер выходит из отставки, чтобы отомстить за убитую собаку.',
                'year': 2014,
                'duration': 101,
                'rating': 7.4,
                'categories': [action_cat, thriller_cat],
                'is_featured': True,
            },
            {
                'title': 'Мстители: Финал',
                'description': 'Оставшиеся в живых Мстители собираются для финальной битвы с Таносом.',
                'year': 2019,
                'duration': 181,
                'rating': 8.4,
                'categories': [action_cat, scifi_cat],
                'is_featured': True,
            },
            {
                'title': 'Джокер',
                'description': 'История происхождения культового злодея из вселенной Бэтмена.',
                'year': 2019,
                'duration': 122,
                'rating': 8.4,
                'categories': [drama_cat, thriller_cat],
                'is_featured': True,
            },
            {
                'title': 'Паразиты',
                'description': 'Бедная семья проникает в жизнь богатой семьи с неожиданными последствиями.',
                'year': 2019,
                'duration': 132,
                'rating': 8.6,
                'categories': [drama_cat, thriller_cat],
                'is_featured': False,
            },
            {
                'title': 'Дюна',
                'description': 'Пол Атрейдес отправляется на опасную планету Арракис, чтобы обеспечить будущее своей семьи.',
                'year': 2021,
                'duration': 155,
                'rating': 8.0,
                'categories': [scifi_cat, drama_cat],
                'is_featured': True,
            },
            {
                'title': 'Оно',
                'description': 'Группа детей сталкивается с древним злом в образе клоуна Пеннивайза.',
                'year': 2017,
                'duration': 135,
                'rating': 7.3,
                'categories': [horror_cat, thriller_cat],
                'is_featured': False,
            },
        ]

        created_count = 0
        for movie_data in additional_movies:
            categories = movie_data.pop('categories')
            film, created = Film.objects.get_or_create(
                title=movie_data['title'],
                defaults=movie_data
            )
            
            if created:
                film.categories.set(categories)
                created_count += 1
                self.stdout.write(f'✓ Добавлен фильм: {film.title} ({film.year})')
            else:
                self.stdout.write(f'⚠ Фильм уже существует: {film.title}')

        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'\n🎬 Добавлено {created_count} дополнительных фильмов!')
            )
            self.stdout.write('Создайте постеры: python manage.py create_all_posters')
        else:
            self.stdout.write(
                self.style.WARNING('Все дополнительные фильмы уже существуют')
            )