from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from films.models import Film
from PIL import Image, ImageDraw, ImageFont
import io
import random


class Command(BaseCommand):
    help = 'Создает красивые placeholder постеры для фильмов без постеров'

    def handle(self, *args, **options):
        self.create_beautiful_placeholders()

    def create_beautiful_placeholders(self):
        """Создает красивые placeholder постеры"""
        self.stdout.write("=" * 70)
        self.stdout.write("🎨 СОЗДАНИЕ КРАСИВЫХ PLACEHOLDER ПОСТЕРОВ")
        self.stdout.write("=" * 70)
        
        # Находим фильмы без постеров
        films_without_posters = Film.objects.filter(poster__isnull=True) | Film.objects.filter(poster='')
        
        self.stdout.write(f"📋 Найдено фильмов без постеров: {films_without_posters.count()}")
        
        # Цветовые схемы для разных жанров
        color_schemes = {
            'семейные': {
                'bg_start': (255, 182, 193),  # Светло-розовый
                'bg_end': (135, 206, 250),    # Небесно-голубой
                'text': (255, 255, 255),      # Белый
                'accent': (255, 215, 0)       # Золотой
            },
            'анимация': {
                'bg_start': (255, 165, 0),    # Оранжевый
                'bg_end': (255, 20, 147),     # Ярко-розовый
                'text': (255, 255, 255),      # Белый
                'accent': (255, 255, 0)       # Желтый
            },
            'боевик': {
                'bg_start': (25, 25, 112),    # Темно-синий
                'bg_end': (0, 0, 0),          # Черный
                'text': (255, 255, 255),      # Белый
                'accent': (255, 0, 0)         # Красный
            },
            'драма': {
                'bg_start': (72, 61, 139),    # Темно-фиолетовый
                'bg_end': (47, 79, 79),       # Темно-серый
                'text': (255, 255, 255),      # Белый
                'accent': (255, 215, 0)       # Золотой
            },
            'default': {
                'bg_start': (70, 130, 180),   # Стальной синий
                'bg_end': (25, 25, 112),      # Темно-синий
                'text': (255, 255, 255),      # Белый
                'accent': (255, 215, 0)       # Золотой
            }
        }
        
        created_count = 0
        for film in films_without_posters:
            try:
                # Определяем цветовую схему на основе категорий
                color_scheme = self.get_color_scheme_for_film(film, color_schemes)
                
                # Создаем постер
                poster_content = self.create_poster(film, color_scheme)
                
                # Сохраняем постер
                filename = f"{film.title.lower().replace(' ', '_')}_placeholder.jpg"
                film.poster.save(
                    filename,
                    ContentFile(poster_content),
                    save=True
                )
                
                self.stdout.write(f"✅ {film.title}: Красивый placeholder создан")
                created_count += 1
                
            except Exception as e:
                self.stdout.write(f"❌ {film.title}: Ошибка - {e}")
        
        self.stdout.write("")
        self.stdout.write(f"✅ Успешно создано постеров: {created_count} из {films_without_posters.count()}")
        
        # Финальная статистика
        self.show_final_statistics()

    def get_color_scheme_for_film(self, film, color_schemes):
        """Определяет цветовую схему для фильма на основе категорий"""
        categories = [cat.name.lower() for cat in film.categories.all()]
        
        if any('семейн' in cat for cat in categories):
            return color_schemes['семейные']
        elif any(cat in ['анимация', 'мультфильм'] for cat in categories):
            return color_schemes['анимация']
        elif any(cat in ['боевик', 'триллер', 'ужасы'] for cat in categories):
            return color_schemes['боевик']
        elif any(cat in ['драма', 'биография'] for cat in categories):
            return color_schemes['драма']
        else:
            return color_schemes['default']

    def create_poster(self, film, color_scheme):
        """Создает красивый постер для фильма"""
        width, height = 400, 600
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Создаем градиентный фон
        for y in range(height):
            # Интерполяция между начальным и конечным цветом
            ratio = y / height
            r = int(color_scheme['bg_start'][0] * (1 - ratio) + color_scheme['bg_end'][0] * ratio)
            g = int(color_scheme['bg_start'][1] * (1 - ratio) + color_scheme['bg_end'][1] * ratio)
            b = int(color_scheme['bg_start'][2] * (1 - ratio) + color_scheme['bg_end'][2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Добавляем декоративные элементы
        self.add_decorative_elements(draw, width, height, color_scheme)
        
        # Добавляем название фильма
        self.add_film_title(draw, film, width, height, color_scheme)
        
        # Добавляем год и рейтинг
        self.add_film_info(draw, film, width, height, color_scheme)
        
        # Добавляем рамку
        draw.rectangle([0, 0, width-1, height-1], outline=color_scheme['accent'], width=3)
        
        # Сохраняем в байты
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=95)
        return img_byte_arr.getvalue()

    def add_decorative_elements(self, draw, width, height, color_scheme):
        """Добавляет декоративные элементы"""
        # Добавляем звезды или круги
        random.seed(42)  # Для воспроизводимости
        for _ in range(20):
            x = random.randint(20, width - 20)
            y = random.randint(20, height - 100)
            size = random.randint(2, 8)
            opacity = random.randint(50, 150)
            
            # Создаем полупрозрачные элементы
            color = (*color_scheme['accent'][:3], opacity) if len(color_scheme['accent']) == 3 else color_scheme['accent']
            draw.ellipse([x-size, y-size, x+size, y+size], fill=color[:3])

    def add_film_title(self, draw, film, width, height, color_scheme):
        """Добавляет название фильма"""
        try:
            # Пытаемся использовать системный шрифт
            font_large = ImageFont.truetype("arial.ttf", 36)
            font_medium = ImageFont.truetype("arial.ttf", 24)
        except:
            # Если не найден, используем стандартный
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
        
        # Разбиваем длинное название на строки
        title_words = film.title.split()
        lines = []
        current_line = ""
        
        for word in title_words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=font_large)
            if bbox[2] - bbox[0] <= width - 40:  # Оставляем отступы
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Рисуем название по центру
        start_y = height // 2 - (len(lines) * 40) // 2
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font_large)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = start_y + i * 40
            
            # Тень для текста
            draw.text((x + 2, y + 2), line, fill=(0, 0, 0), font=font_large)
            # Основной текст
            draw.text((x, y), line, fill=color_scheme['text'], font=font_large)

    def add_film_info(self, draw, film, width, height, color_scheme):
        """Добавляет информацию о фильме"""
        try:
            font_small = ImageFont.truetype("arial.ttf", 18)
        except:
            font_small = ImageFont.load_default()
        
        # Год выпуска
        year_text = str(film.year)
        bbox = draw.textbbox((0, 0), year_text, font=font_small)
        year_width = bbox[2] - bbox[0]
        year_x = (width - year_width) // 2
        year_y = height - 100
        
        draw.text((year_x + 1, year_y + 1), year_text, fill=(0, 0, 0), font=font_small)
        draw.text((year_x, year_y), year_text, fill=color_scheme['accent'], font=font_small)
        
        # Рейтинг (если есть)
        if film.rating and film.rating > 0:
            rating_text = f"⭐ {film.rating}"
            bbox = draw.textbbox((0, 0), rating_text, font=font_small)
            rating_width = bbox[2] - bbox[0]
            rating_x = (width - rating_width) // 2
            rating_y = year_y + 25
            
            draw.text((rating_x + 1, rating_y + 1), rating_text, fill=(0, 0, 0), font=font_small)
            draw.text((rating_x, rating_y), rating_text, fill=color_scheme['accent'], font=font_small)
        
        # Категории
        categories = list(film.categories.all())
        if categories:
            cat_text = categories[0].name
            bbox = draw.textbbox((0, 0), cat_text, font=font_small)
            cat_width = bbox[2] - bbox[0]
            cat_x = (width - cat_width) // 2
            cat_y = height - 50
            
            draw.text((cat_x + 1, cat_y + 1), cat_text, fill=(0, 0, 0), font=font_small)
            draw.text((cat_x, cat_y), cat_text, fill=color_scheme['text'], font=font_small)

    def show_final_statistics(self):
        """Показывает финальную статистику"""
        total_films = Film.objects.count()
        films_with_posters = Film.objects.exclude(poster='').exclude(poster=None).count()
        films_without_posters = total_films - films_with_posters
        
        self.stdout.write("")
        self.stdout.write("=" * 70)
        self.stdout.write("📊 ФИНАЛЬНАЯ СТАТИСТИКА")
        self.stdout.write("=" * 70)
        self.stdout.write(f"🎬 Всего фильмов: {total_films}")
        self.stdout.write(f"✅ С постерами: {films_with_posters}")
        self.stdout.write(f"❌ Без постеров: {films_without_posters}")
        self.stdout.write(f"📈 Покрытие: {(films_with_posters/total_films)*100:.1f}%")
        
        if films_without_posters == 0:
            self.stdout.write("")
            self.stdout.write("🎉 ПОЗДРАВЛЯЕМ! У всех фильмов есть постеры!")
        
        self.stdout.write("")
        self.stdout.write("🌐 Проверить результат:")
        self.stdout.write("   • Админка: http://127.0.0.1:8000/admin/")
        self.stdout.write("   • Сайт: http://127.0.0.1:8000/")