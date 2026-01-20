from django.core.management.base import BaseCommand
from films.models import Actor, Film
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont
import tempfile
import os
from datetime import date


class Command(BaseCommand):
    help = 'Добавляет актеров с биографиями и фотографиями'

    def handle(self, *args, **options):
        self.add_famous_actors()

    def create_actor_photo(self, name, width=300, height=400):
        """Создает фотографию актера с именем"""
        # Цветовые схемы для разных актеров
        color_schemes = [
            {'bg': '#2c3e50', 'text': '#ecf0f1', 'accent': '#3498db'},
            {'bg': '#8e44ad', 'text': '#ecf0f1', 'accent': '#e74c3c'},
            {'bg': '#27ae60', 'text': '#ecf0f1', 'accent': '#f39c12'},
            {'bg': '#e67e22', 'text': '#ecf0f1', 'accent': '#9b59b6'},
            {'bg': '#34495e', 'text': '#ecf0f1', 'accent': '#1abc9c'},
            {'bg': '#c0392b', 'text': '#ecf0f1', 'accent': '#f1c40f'},
        ]
        
        # Выбираем цветовую схему на основе хеша имени
        scheme = color_schemes[hash(name) % len(color_schemes)]
        
        # Создаем изображение
        img = Image.new('RGB', (width, height), color=scheme['bg'])
        draw = ImageDraw.Draw(img)
        
        # Создаем градиент
        for y in range(height):
            alpha = y / height * 0.3
            r1, g1, b1 = tuple(int(scheme['bg'][i:i+2], 16) for i in (1, 3, 5))
            r2, g2, b2 = tuple(int(scheme['accent'][i:i+2], 16) for i in (1, 3, 5))
            
            r = int(r1 * (1 - alpha) + r2 * alpha)
            g = int(g1 * (1 - alpha) + g2 * alpha)
            b = int(b1 * (1 - alpha) + b2 * alpha)
            
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Загружаем шрифты
        try:
            name_font = ImageFont.truetype("arial.ttf", 24)
            label_font = ImageFont.truetype("arial.ttf", 16)
        except:
            name_font = ImageFont.load_default()
            label_font = ImageFont.load_default()
        
        # Рамка
        draw.rectangle([(10, 10), (width-10, height-10)], outline=scheme['text'], width=2)
        
        # Метка "АКТЕР"
        label_text = "АКТЕР"
        bbox = draw.textbbox((0, 0), label_text, font=label_font)
        label_width = bbox[2] - bbox[0]
        label_x = (width - label_width) // 2
        draw.text((label_x, 30), label_text, fill=scheme['accent'], font=label_font)
        
        # Имя актера
        words = name.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=name_font)
            if bbox[2] - bbox[0] <= width - 40:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Рисуем имя по центру
        total_text_height = len(lines) * 30
        start_y = (height - total_text_height) // 2
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=name_font)
            line_width = bbox[2] - bbox[0]
            line_x = (width - line_width) // 2
            line_y = start_y + i * 30
            
            # Тень
            draw.text((line_x + 2, line_y + 2), line, fill='black', font=name_font)
            # Основной текст
            draw.text((line_x, line_y), line, fill=scheme['text'], font=name_font)
        
        # Декоративные элементы
        draw.line([(30, 70), (width - 30, 70)], fill=scheme['accent'], width=2)
        draw.line([(30, height - 50), (width - 30, height - 50)], fill=scheme['accent'], width=2)
        
        return img

    def add_famous_actors(self):
        """Добавляет знаменитых актеров"""
        actors_data = [
            {
                'name': 'Леонардо ДиКаприо',
                'birth_date': date(1974, 11, 11),
                'birth_place': 'Лос-Анджелес, Калифорния, США',
                'height': 183,
                'biography': '''Леонардо Вильгельм ДиКаприо — американский актёр и продюсер. Лауреат премии «Оскар» (2016), трёх премий «Золотой глобус» и премии BAFTA. 

Начал карьеру в конце 1980-х, снявшись в нескольких рекламных роликах и образовательных фильмах. В начале 1990-х получил роли в телесериалах, а затем дебютировал в кино в фильме "Твари 3" (1991).

Мировую известность получил после роли Джека Доусона в фильме "Титаник" (1997) Джеймса Кэмерона. Фильм стал одним из самых кассовых в истории кинематографа.

Известен своим сотрудничеством с режиссёрами Мартином Скорсезе, Кристофером Ноланом и Алехандро Гонсалесом Иньярриту. Активист в области защиты окружающей среды.''',
                'awards': 'Оскар за лучшую мужскую роль (2016), 3 Золотых глобуса, BAFTA, премия Гильдии киноактёров США',
                'films': ['Начало', 'Титаник']
            },
            {
                'name': 'Роберт Дауни мл.',
                'birth_date': date(1965, 4, 4),
                'birth_place': 'Нью-Йорк, США',
                'height': 174,
                'biography': '''Роберт Джон Дауни-младший — американский актёр и продюсер. Наиболее известен по роли Тони Старка / Железного человека в кинематографической вселенной Marvel.

Начал актёрскую карьеру в детстве, снявшись в фильме отца "Паунд" (1970). В 1980-х и 1990-х годах снимался в различных фильмах, но карьера была прервана из-за проблем с наркотиками.

Возвращение к актёрской деятельности началось в 2000-х годах. Настоящий успех пришёл с ролью Железного человека в 2008 году, которая сделала его одним из самых высокооплачиваемых актёров Голливуда.

Также известен по ролям в фильмах о Шерлоке Холмсе режиссёра Гая Ричи и комедии "Тропический гром".''',
                'awards': 'Золотой глобус (2001), премия BAFTA, номинант на Оскар (1993)',
                'films': ['Мстители: Финал']
            },
            {
                'name': 'Мэттью МакКонахи',
                'birth_date': date(1969, 11, 4),
                'birth_place': 'Ювалде, Техас, США',
                'height': 182,
                'biography': '''Мэттью Дэвид МакКонахи — американский актёр и продюсер. Лауреат премии «Оскар» за лучшую мужскую роль.

Дебютировал в кино в 1993 году в фильме "Под кайфом и в смятении" Ричарда Линклейтера. В 1990-х и 2000-х годах в основном снимался в романтических комедиях и боевиках.

Кардинальный поворот в карьере произошёл в 2010-х годах, когда актёр начал выбирать более серьёзные драматические роли. Этот период называют "МакКонессанс".

Получил "Оскар" за роль в фильме "Далласский клуб покупателей" (2013). Также известен по ролям в "Интерстеллар", "Настоящий детектив" и "Волк с Уолл-стрит".''',
                'awards': 'Оскар за лучшую мужскую роль (2014), Золотой глобус, премия Гильдии киноактёров США',
                'films': ['Интерстеллар']
            },
            {
                'name': 'Брэд Питт',
                'birth_date': date(1963, 12, 18),
                'birth_place': 'Шони, Оклахома, США',
                'height': 180,
                'biography': '''Уильям Брэдли "Брэд" Питт — американский актёр и кинопродюсер. Лауреат премии «Оскар» и двух премий «Золотой глобус».

Начал карьеру в конце 1980-х с небольших ролей в телесериалах. Прорыв произошёл после роли в фильме "Тельма и Луиза" (1991).

Стал одним из самых узнаваемых и влиятельных актёров Голливуда благодаря ролям в фильмах "Интервью с вампиром", "Семь", "Бойцовский клуб", "Океан одиннадцати".

Как продюсер основал компанию Plan B Entertainment, которая выпустила множество успешных фильмов, включая "12 лет рабства" и "Лунный свет".''',
                'awards': 'Оскар за лучшую мужскую роль второго плана (2020), 2 Золотых глобуса, премия BAFTA',
                'films': ['Бойцовский клуб', 'Семь']
            },
            {
                'name': 'Том Хэнкс',
                'birth_date': date(1956, 7, 9),
                'birth_place': 'Конкорд, Калифорния, США',
                'height': 183,
                'biography': '''Томас Джеффри "Том" Хэнкс — американский актёр, режиссёр и продюсер. Двукратный лауреат премии «Оскар» за лучшую мужскую роль.

Начал карьеру в театре, затем перешёл на телевидение. Первый успех в кино пришёл с комедией "Всплеск" (1984).

Стал одним из самых любимых и уважаемых актёров Америки благодаря ролям в фильмах "Форрест Гамп", "Филадельфия", "Спасти рядового Райана", "Изгой".

Известен своей способностью играть обычных американцев, попадающих в необычные обстоятельства. Часто называется "самым порядочным человеком Голливуда".''',
                'awards': '2 Оскара за лучшую мужскую роль (1994, 1995), 4 Золотых глобуса, премия Кеннеди-центра',
                'films': ['Форрест Гамп']
            },
            {
                'name': 'Морган Фриман',
                'birth_date': date(1937, 6, 1),
                'birth_place': 'Мемфис, Теннесси, США',
                'height': 188,
                'biography': '''Морган Фриман — американский актёр, режиссёр и рассказчик. Лауреат премии «Оскар» и премии «Золотой глобус».

Начал карьеру в театре в 1960-х годах. Долгое время играл в театральных постановках, прежде чем перейти в кино.

Получил широкое признание в 1980-х годах благодаря ролям в фильмах "Уличный мудрец" и "Шофёр мисс Дэйзи".

Стал одним из самых узнаваемых актёров Голливуда благодаря своему характерному голосу и харизматичному присутствию на экране. Известен по ролям в "Побег из Шоушенка", "Семь", "Миллион долларов, детка".''',
                'awards': 'Оскар за лучшую мужскую роль второго плана (2005), Золотой глобус, премия Гильдии киноактёров США',
                'films': ['Побег из Шоушенка', 'Семь']
            }
        ]

        for actor_data in actors_data:
            # Проверяем, существует ли уже такой актёр
            if Actor.objects.filter(name=actor_data['name']).exists():
                self.stdout.write(f"Актёр {actor_data['name']} уже существует")
                continue

            # Создаём фотографию актёра
            photo_img = self.create_actor_photo(actor_data['name'])
            
            # Сохраняем во временный файл
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                photo_img.save(temp_file.name, 'JPEG', quality=85)
                temp_path = temp_file.name

            # Создаём актёра
            actor = Actor.objects.create(
                name=actor_data['name'],
                birth_date=actor_data['birth_date'],
                birth_place=actor_data['birth_place'],
                height=actor_data['height'],
                biography=actor_data['biography'],
                awards=actor_data['awards']
            )

            # Добавляем фотографию
            filename = f"{actor_data['name'].lower().replace(' ', '_')}_photo.jpg"
            with open(temp_path, 'rb') as f:
                actor.photo.save(filename, File(f))

            # Удаляем временный файл
            os.unlink(temp_path)

            # Связываем с фильмами
            for film_title in actor_data['films']:
                try:
                    film = Film.objects.get(title=film_title)
                    actor.films.add(film)
                    self.stdout.write(f"Связал {actor.name} с фильмом {film.title}")
                except Film.DoesNotExist:
                    self.stdout.write(f"Фильм '{film_title}' не найден для актёра {actor.name}")

            self.stdout.write(f"✅ Добавлен актёр: {actor.name}")

        self.stdout.write(f"\n✅ Добавление актёров завершено!")
        
        # Показываем статистику
        actors_count = Actor.objects.count()
        self.stdout.write(f"Всего актёров в базе: {actors_count}")
        
        for actor in Actor.objects.all():
            films_count = actor.films.count()
            self.stdout.write(f"  {actor.name}: {films_count} фильмов")