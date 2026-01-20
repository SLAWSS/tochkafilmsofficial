from django.core.management.base import BaseCommand
from films.models import Category, Film


class Command(BaseCommand):
    help = 'Создает тестовые данные для сайта'

    def handle(self, *args, **kwargs):
        # Создаем категории
        categories_data = [
            ('Боевик', 'action'),
            ('Комедия', 'comedy'),
            ('Драма', 'drama'),
            ('Фантастика', 'sci-fi'),
            ('Триллер', 'thriller'),
            ('Ужасы', 'horror'),
        ]
        
        categories = {}
        for name, slug in categories_data:
            cat, created = Category.objects.get_or_create(name=name, slug=slug)
            categories[slug] = cat
            if created:
                self.stdout.write(f'Создана категория: {name}')

        # Создаем фильмы
        films_data = [
            {
                'title': 'Начало',
                'description': 'Кобб — талантливый вор, лучший из лучших в опасном искусстве извлечения: он крадет ценные секреты из глубин подсознания во время сна.',
                'year': 2010,
                'duration': 148,
                'rating': 8.8,
                'categories': ['action', 'sci-fi', 'thriller'],
                'is_featured': True,
            },
            {
                'title': 'Интерстеллар',
                'description': 'Когда засуха приводит человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину в путешествие.',
                'year': 2014,
                'duration': 169,
                'rating': 8.6,
                'categories': ['sci-fi', 'drama'],
                'is_featured': True,
            },
            {
                'title': 'Темный рыцарь',
                'description': 'Бэтмен поднимает ставки в войне с криминалом. С помощью лейтенанта Джима Гордона и прокурора Харви Дента он намерен очистить улицы от преступности.',
                'year': 2008,
                'duration': 152,
                'rating': 9.0,
                'categories': ['action', 'thriller', 'drama'],
                'is_featured': True,
            },
            {
                'title': 'Побег из Шоушенка',
                'description': 'Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью.',
                'year': 1994,
                'duration': 142,
                'rating': 9.3,
                'categories': ['drama'],
                'is_featured': True,
            },
            {
                'title': 'Форрест Гамп',
                'description': 'От лица главного героя Форреста Гампа, слабоумного безобидного человека с благородным и открытым сердцем, рассказывается история его необыкновенной жизни.',
                'year': 1994,
                'duration': 142,
                'rating': 8.8,
                'categories': ['drama', 'comedy'],
                'is_featured': False,
            },
            {
                'title': 'Матрица',
                'description': 'Жизнь Томаса Андерсона разделена на две части: днём он — самый обычный офисный работник, получающий нагоняи от начальства, а ночью превращается в хакера.',
                'year': 1999,
                'duration': 136,
                'rating': 8.7,
                'categories': ['action', 'sci-fi'],
                'is_featured': True,
            },
            {
                'title': 'Криминальное чтиво',
                'description': 'Двое бандитов Винсент Вега и Джулс Винфилд ведут философские беседы в перерывах между разборками и решением проблем с должниками криминального босса.',
                'year': 1994,
                'duration': 154,
                'rating': 8.9,
                'categories': ['thriller', 'drama'],
                'is_featured': False,
            },
            {
                'title': 'Бойцовский клуб',
                'description': 'Сотрудник страховой компании страдает хронической бессонницей и отчаянно пытается вырваться из мучительно скучной жизни.',
                'year': 1999,
                'duration': 139,
                'rating': 8.8,
                'categories': ['drama', 'thriller'],
                'is_featured': False,
            },
        ]

        for film_data in films_data:
            cat_slugs = film_data.pop('categories')
            film, created = Film.objects.get_or_create(
                title=film_data['title'],
                defaults=film_data
            )
            
            if created:
                for slug in cat_slugs:
                    if slug in categories:
                        film.categories.add(categories[slug])
                self.stdout.write(f'Создан фильм: {film.title}')

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы!'))
