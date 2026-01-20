from django.core.management.base import BaseCommand
from films.models import Film, Category
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont
import tempfile
import os


class Command(BaseCommand):
    help = 'Добавляет 30 семейных фильмов'

    def handle(self, *args, **options):
        self.add_family_films()

    def create_family_poster(self, title, year, width=300, height=450):
        """Создает постер для семейного фильма"""
        # Яркие семейные цветовые схемы
        color_schemes = [
            {'bg': '#FF6B6B', 'secondary': '#4ECDC4', 'text': '#FFFFFF', 'accent': '#45B7D1'},
            {'bg': '#96CEB4', 'secondary': '#FFEAA7', 'text': '#2D3436', 'accent': '#6C5CE7'},
            {'bg': '#FD79A8', 'secondary': '#FDCB6E', 'text': '#FFFFFF', 'accent': '#00B894'},
            {'bg': '#74B9FF', 'secondary': '#A29BFE', 'text': '#FFFFFF', 'accent': '#00CEC9'},
            {'bg': '#55A3FF', 'secondary': '#FD79A8', 'text': '#FFFFFF', 'accent': '#FDCB6E'},
            {'bg': '#00B894', 'secondary': '#00CEC9', 'text': '#FFFFFF', 'accent': '#FFEAA7'},
        ]
        
        scheme = color_schemes[hash(title) % len(color_schemes)]
        
        # Создаем изображение с градиентом
        img = Image.new('RGB', (width, height), color=scheme['bg'])
        draw = ImageDraw.Draw(img)
        
        # Создаем радиальный градиент
        for y in range(height):
            for x in range(width):
                # Расстояние от центра
                center_x, center_y = width // 2, height // 2
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                max_distance = (width ** 2 + height ** 2) ** 0.5 / 2
                
                # Интерполяция цветов
                ratio = min(distance / max_distance, 1.0)
                
                # Парсим цвета
                bg_r, bg_g, bg_b = tuple(int(scheme['bg'][i:i+2], 16) for i in (1, 3, 5))
                sec_r, sec_g, sec_b = tuple(int(scheme['secondary'][i:i+2], 16) for i in (1, 3, 5))
                
                r = int(bg_r * (1 - ratio) + sec_r * ratio)
                g = int(bg_g * (1 - ratio) + sec_g * ratio)
                b = int(bg_b * (1 - ratio) + sec_b * ratio)
                
                if y % 3 == 0 and x % 3 == 0:  # Оптимизация
                    draw.point((x, y), fill=(r, g, b))
        
        # Загружаем шрифты
        try:
            title_font = ImageFont.truetype("arial.ttf", 26)
            year_font = ImageFont.truetype("arial.ttf", 18)
            label_font = ImageFont.truetype("arial.ttf", 14)
        except:
            title_font = ImageFont.load_default()
            year_font = ImageFont.load_default()
            label_font = ImageFont.load_default()
        
        # Рамка
        draw.rectangle([(8, 8), (width-8, height-8)], outline=scheme['text'], width=3)
        
        # Семейная метка
        label_text = "СЕМЕЙНЫЙ ФИЛЬМ"
        bbox = draw.textbbox((0, 0), label_text, font=label_font)
        label_width = bbox[2] - bbox[0]
        label_x = (width - label_width) // 2
        
        # Фон для метки
        draw.rectangle([(label_x - 10, 25), (label_x + label_width + 10, 45)], 
                      fill=scheme['accent'], outline=scheme['text'], width=1)
        draw.text((label_x, 28), label_text, fill=scheme['text'], font=label_font)
        
        # Название фильма
        words = title.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=title_font)
            if bbox[2] - bbox[0] <= width - 40:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Рисуем название
        total_text_height = len(lines) * 32
        start_y = (height - total_text_height) // 2
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=title_font)
            line_width = bbox[2] - bbox[0]
            line_x = (width - line_width) // 2
            line_y = start_y + i * 32
            
            # Тень
            draw.text((line_x + 2, line_y + 2), line, fill='black', font=title_font)
            # Основной текст
            draw.text((line_x, line_y), line, fill=scheme['text'], font=title_font)
        
        # Год
        year_text = str(year)
        bbox = draw.textbbox((0, 0), year_text, font=year_font)
        year_width = bbox[2] - bbox[0]
        year_x = (width - year_width) // 2
        year_y = height - 60
        
        # Фон для года
        draw.rectangle([(year_x - 15, year_y - 5), (year_x + year_width + 15, year_y + 25)], 
                      fill=scheme['accent'], outline=scheme['text'], width=1)
        draw.text((year_x, year_y), year_text, fill=scheme['text'], font=year_font)
        
        # Декоративные звездочки
        star_positions = [(30, 80), (width-40, 100), (50, height-100), (width-60, height-80)]
        for x, y in star_positions:
            draw.text((x, y), "⭐", fill=scheme['accent'], font=year_font)
        
        return img

    def get_family_films_data(self):
        """Возвращает данные о семейных фильмах"""
        return [
            {
                'title': 'Холодное сердце',
                'year': 2013,
                'duration': 102,
                'rating': 8.2,
                'description': 'Анимационный мюзикл Disney о двух сестрах-принцессах Эльзе и Анне. Эльза обладает магической способностью создавать лед и снег, но после несчастного случая скрывает свои силы. Когда тайна раскрывается, Эльза случайно погружает королевство в вечную зиму.',
                'trailer_url': 'https://rutube.ru/video/frozen_2013_russian_trailer_hd/'
            },
            {
                'title': 'Холодное сердце 2',
                'year': 2019,
                'duration': 103,
                'rating': 8.0,
                'description': 'Продолжение приключений Эльзы и Анны. Эльза слышит загадочный голос, зовущий её на север. Вместе с Анной, Кристоффом, Олафом и Свеном она отправляется в опасное путешествие в Зачарованный лес, чтобы найти источник голоса.',
                'trailer_url': 'https://rutube.ru/video/frozen_2_2019_russian_trailer_hd/'
            },
            {
                'title': 'Моана',
                'year': 2016,
                'duration': 107,
                'rating': 8.1,
                'description': 'Приключения отважной полинезийской девочки Моаны, которая отправляется в опасное морское путешествие, чтобы спасти свой остров. В пути её сопровождает полубог Мауи.',
                'trailer_url': 'https://rutube.ru/video/moana_2016_russian_trailer_hd/'
            },
            {
                'title': 'Зверополис',
                'year': 2016,
                'duration': 108,
                'rating': 8.3,
                'description': 'В городе Зверополисе, где хищники и травоядные живут вместе, крольчиха Джуди Хоппс становится первым кроликом-полицейским. Она объединяется с лисом-мошенником Ником Уайлдом, чтобы раскрыть заговор.',
                'trailer_url': 'https://rutube.ru/video/zootopia_2016_russian_trailer_hd/'
            },
            {
                'title': 'Тайная жизнь домашних животных',
                'year': 2016,
                'duration': 87,
                'rating': 7.8,
                'description': 'Комедия о том, что делают домашние животные, когда их хозяева уходят на работу. Терьер Макс живет счастливой жизнью, пока его хозяйка не приводит домой нового питомца - дворнягу Дюка.',
                'trailer_url': 'https://rutube.ru/video/secret_life_pets_2016_russian_trailer/'
            },
            {
                'title': 'Тайная жизнь домашних животных 2',
                'year': 2019,
                'duration': 86,
                'rating': 7.5,
                'description': 'Продолжение приключений Макса и его друзей. Теперь у Макса появляется новая задача - защищать маленького хозяина Лиама. Тем временем Гиджет пытается спасти любимую игрушку Макса.',
                'trailer_url': 'https://rutube.ru/video/secret_life_pets_2_2019_russian_trailer/'
            },
            {
                'title': 'Коко',
                'year': 2017,
                'duration': 105,
                'rating': 8.7,
                'description': 'Мигель мечтает стать музыкантом, но его семья запрещает музыку. В День мертвых он попадает в Страну мертвых, где встречает своих предков и раскрывает семейную тайну.',
                'trailer_url': 'https://rutube.ru/video/coco_2017_russian_trailer_hd/'
            },
            {
                'title': 'Головоломка',
                'year': 2015,
                'duration': 95,
                'rating': 8.6,
                'description': 'Анимационный фильм Pixar о эмоциях 11-летней девочки Райли. Радость, Печаль, Страх, Гнев и Брезгливость управляют её поведением из штаб-квартиры в голове.',
                'trailer_url': 'https://rutube.ru/video/inside_out_2015_russian_trailer_hd/'
            },
            {
                'title': 'Тачки',
                'year': 2006,
                'duration': 117,
                'rating': 7.8,
                'description': 'Молния МакКуин - гоночная машина, мечтающая выиграть Кубок Поршня. По пути на решающую гонку он случайно попадает в забытый городок Радиатор-Спрингс.',
                'trailer_url': 'https://rutube.ru/video/cars_2006_russian_trailer_hd/'
            },
            {
                'title': 'Тачки 2',
                'year': 2011,
                'duration': 106,
                'rating': 7.2,
                'description': 'Молния МакКуин отправляется в кругосветное путешествие для участия в Гран-при мира. Его сопровождает лучший друг Мэтр, который случайно оказывается втянут в шпионскую интригу.',
                'trailer_url': 'https://rutube.ru/video/cars_2_2011_russian_trailer_hd/'
            },
            {
                'title': 'Тачки 3',
                'year': 2017,
                'duration': 102,
                'rating': 7.4,
                'description': 'Молния МакКуин сталкивается с новым поколением высокотехнологичных гонщиков. Чтобы вернуться в игру, ему нужна помощь молодого тренера Круз Рамирес.',
                'trailer_url': 'https://rutube.ru/video/cars_3_2017_russian_trailer_hd/'
            },
            {
                'title': 'Рататуй',
                'year': 2007,
                'duration': 111,
                'rating': 8.5,
                'description': 'Крыса Реми мечтает стать поваром в парижском ресторане. Он объединяется с неуклюжим поваренком Лингвини, чтобы создавать кулинарные шедевры.',
                'trailer_url': 'https://rutube.ru/video/ratatouille_2007_russian_trailer_hd/'
            },
            {
                'title': 'ВАЛЛ-И',
                'year': 2008,
                'duration': 98,
                'rating': 8.8,
                'description': 'В далеком будущем робот ВАЛЛ-И остался один на заброшенной Земле. Его жизнь меняется, когда он встречает робота-разведчика ЕВУ и следует за ней в космическое путешествие.',
                'trailer_url': 'https://rutube.ru/video/wall_e_2008_russian_trailer_hd/'
            },
            {
                'title': 'Вверх',
                'year': 2009,
                'duration': 96,
                'rating': 8.7,
                'description': '78-летний Карл Фредриксен привязывает тысячи воздушных шаров к своему дому и отправляется в Южную Америку. Неожиданно с ним путешествует 8-летний скаут Рассел.',
                'trailer_url': 'https://rutube.ru/video/up_2009_russian_trailer_hd/'
            },
            {
                'title': 'Университет монстров',
                'year': 2013,
                'duration': 104,
                'rating': 7.9,
                'description': 'Приквел к "Корпорации монстров". Майк и Салли учатся в университете и не могут терпеть друг друга, но обстоятельства заставляют их работать в команде.',
                'trailer_url': 'https://rutube.ru/video/monsters_university_2013_russian_trailer/'
            },
            {
                'title': 'Хороший динозавр',
                'year': 2015,
                'duration': 93,
                'rating': 7.6,
                'description': 'В мире, где динозавры не вымерли, молодой апатозавр Арло подружился с человеческим мальчиком. Вместе они отправляются в путешествие домой.',
                'trailer_url': 'https://rutube.ru/video/good_dinosaur_2015_russian_trailer/'
            },
            {
                'title': 'Суперсемейка',
                'year': 2004,
                'duration': 115,
                'rating': 8.4,
                'description': 'Семья супергероев вынуждена скрывать свои способности и жить обычной жизнью. Но когда миру угрожает опасность, им приходится снова стать героями.',
                'trailer_url': 'https://rutube.ru/video/incredibles_2004_russian_trailer_hd/'
            },
            {
                'title': 'Суперсемейка 2',
                'year': 2018,
                'duration': 125,
                'rating': 8.1,
                'description': 'Эластика получает новую миссию, а мистер Исключительный остается дома с детьми. Тем временем семье угрожает новый злодей - Гипнотизер.',
                'trailer_url': 'https://rutube.ru/video/incredibles_2_2018_russian_trailer_hd/'
            },
            {
                'title': 'Гадкий я',
                'year': 2010,
                'duration': 95,
                'rating': 8.0,
                'description': 'Суперзлодей Грю планирует украсть Луну, но его планы рушатся, когда он усыновляет трех девочек-сирот. Ему помогают желтые миньоны.',
                'trailer_url': 'https://rutube.ru/video/despicable_me_2010_russian_trailer_hd/'
            },
            {
                'title': 'Гадкий я 2',
                'year': 2013,
                'duration': 98,
                'rating': 7.8,
                'description': 'Грю оставил злодейство и воспитывает дочерей. Антизлодейская лига вербует его для поимки нового суперзлодея. Его партнером становится агент Люси.',
                'trailer_url': 'https://rutube.ru/video/despicable_me_2_2013_russian_trailer_hd/'
            },
            {
                'title': 'Гадкий я 3',
                'year': 2017,
                'duration': 90,
                'rating': 7.5,
                'description': 'Грю встречает своего брата-близнеца Дрю и узнает о семейной традиции злодейства. Тем временем его жена Люси пытается стать хорошей мамой для девочек.',
                'trailer_url': 'https://rutube.ru/video/despicable_me_3_2017_russian_trailer_hd/'
            },
            {
                'title': 'Миньоны',
                'year': 2015,
                'duration': 91,
                'rating': 7.7,
                'description': 'Предыстория миньонов - желтых существ, которые всегда служили самым отъявленным злодеям. Кевин, Стюарт и Боб отправляются искать нового хозяина.',
                'trailer_url': 'https://rutube.ru/video/minions_2015_russian_trailer_hd/'
            },
            {
                'title': 'Как приручить дракона',
                'year': 2010,
                'duration': 98,
                'rating': 8.5,
                'description': 'Подросток-викинг Иккинг не похож на других воинов своего племени. Вместо того чтобы убить дракона, он подружился с ним и назвал Беззубиком.',
                'trailer_url': 'https://rutube.ru/video/how_train_dragon_2010_russian_trailer/'
            },
            {
                'title': 'Как приручить дракона 2',
                'year': 2014,
                'duration': 102,
                'rating': 8.3,
                'description': 'Иккинг и Беззубик исследуют новые земли и встречают таинственного всадника на драконе, который оказывается матерью Иккинга. Им угрожает новый враг - Драго.',
                'trailer_url': 'https://rutube.ru/video/how_train_dragon_2_2014_russian_trailer/'
            },
            {
                'title': 'Как приручить дракона 3',
                'year': 2019,
                'duration': 104,
                'rating': 8.0,
                'description': 'Заключительная часть трилогии. Иккинг стал вождем, а Беззубик встретил самку своего вида - Дневную Фурию. Героям предстоит найти скрытый мир драконов.',
                'trailer_url': 'https://rutube.ru/video/how_train_dragon_3_2019_russian_trailer/'
            },
            {
                'title': 'Кунг-фу Панда',
                'year': 2008,
                'duration': 92,
                'rating': 8.2,
                'description': 'Ленивый панда По случайно становится избранным воином Дракона. Ему предстоит обучиться кунг-фу у Неистовой Пятерки и победить злого снежного барса Тай Лунга.',
                'trailer_url': 'https://rutube.ru/video/kung_fu_panda_2008_russian_trailer_hd/'
            },
            {
                'title': 'Кунг-фу Панда 2',
                'year': 2011,
                'duration': 91,
                'rating': 8.0,
                'description': 'По и Неистовая Пятерка сражаются с павлином Шэнем, который хочет завоевать Китай с помощью пушек. По узнает правду о своем прошлом.',
                'trailer_url': 'https://rutube.ru/video/kung_fu_panda_2_2011_russian_trailer_hd/'
            },
            {
                'title': 'Кунг-фу Панда 3',
                'year': 2016,
                'duration': 95,
                'rating': 7.8,
                'description': 'По встречает своего биологического отца и попадает в секретную деревню панд. Ему предстоит научиться быть настоящей пандой и победить злого духа Кая.',
                'trailer_url': 'https://rutube.ru/video/kung_fu_panda_3_2016_russian_trailer_hd/'
            },
            {
                'title': 'Семейка Крудс',
                'year': 2013,
                'duration': 98,
                'rating': 7.9,
                'description': 'Семья пещерных людей отправляется в путешествие в поисках нового дома после того, как их пещера была разрушена. Их ведет изобретательный мальчик Гай.',
                'trailer_url': 'https://rutube.ru/video/croods_2013_russian_trailer_hd/'
            },
            {
                'title': 'Семейка Крудс: Новоселье',
                'year': 2020,
                'duration': 95,
                'rating': 7.6,
                'description': 'Семья Крудс находит идеальное место для жизни, но оказывается, что там уже живет другая семья - Лучшие. Между семьями разгорается соперничество.',
                'trailer_url': 'https://rutube.ru/video/croods_new_age_2020_russian_trailer_hd/'
            }
        ]

    def add_family_films(self):
        """Добавляет семейные фильмы"""
        # Создаем или получаем категорию "Семейные"
        family_category, created = Category.objects.get_or_create(
            name="Семейные",
            defaults={'slug': 'family'}
        )
        
        if created:
            self.stdout.write("✅ Создана категория 'Семейные'")
        
        films_data = self.get_family_films_data()
        added_count = 0
        
        for film_data in films_data:
            # Проверяем, существует ли уже такой фильм
            if Film.objects.filter(title=film_data['title']).exists():
                self.stdout.write(f"Фильм '{film_data['title']}' уже существует")
                continue
            
            # Создаем постер
            poster_img = self.create_family_poster(film_data['title'], film_data['year'])
            
            # Сохраняем во временный файл
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                poster_img.save(temp_file.name, 'JPEG', quality=85)
                temp_path = temp_file.name
            
            # Создаем фильм
            film = Film.objects.create(
                title=film_data['title'],
                description=film_data['description'],
                year=film_data['year'],
                duration=film_data['duration'],
                rating=film_data['rating'],
                trailer_url=film_data['trailer_url']
            )
            
            # Добавляем постер
            filename = f"{film_data['title'].lower().replace(' ', '_').replace(':', '')}_family_poster.jpg"
            with open(temp_path, 'rb') as f:
                film.poster.save(filename, File(f))
            
            # Добавляем к семейной категории
            film.categories.add(family_category)
            
            # Удаляем временный файл
            os.unlink(temp_path)
            
            added_count += 1
            self.stdout.write(f"✅ Добавлен фильм: {film.title} ({film.year})")
        
        self.stdout.write(f"\n🎬 Добавлено {added_count} семейных фильмов!")
        
        # Показываем статистику
        total_family_films = Film.objects.filter(categories=family_category).count()
        self.stdout.write(f"Всего семейных фильмов в базе: {total_family_films}")
        
        # Показываем примеры
        self.stdout.write(f"\n📋 ПРИМЕРЫ ДОБАВЛЕННЫХ ФИЛЬМОВ:")
        recent_films = Film.objects.filter(categories=family_category).order_by('-created_at')[:5]
        for film in recent_films:
            self.stdout.write(f"  • {film.title} ({film.year}) - ⭐ {film.rating}")