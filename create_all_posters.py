import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from films.models import Film
from django.conf import settings
import io
import random


class Command(BaseCommand):
    help = 'Создает красивые постеры для всех фильмов'

    def transliterate_filename(self, text):
        """Транслитерирует русский текст в латиницу"""
        replacements = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
            'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', ' ': '_'
        }
        result = text.lower()
        for ru, en in replacements.items():
            result = result.replace(ru, en)
        # Убираем цифры из имени файла для красоты
        result = ''.join(c for c in result if c.isalpha() or c == '_')
        return result

    def get_genre_colors(self, film):
        """Возвращает цвета в зависимости от жанра фильма"""
        categories = [cat.name.lower() for cat in film.categories.all()]
        
        if 'ужасы' in categories or 'horror' in categories:
            return [(139, 0, 0), (0, 0, 0)]  # Темно-красный к черному
        elif 'боевик' in categories or 'action' in categories:
            return [(255, 140, 0), (139, 69, 19)]  # Оранжевый к коричневому
        elif 'комедия' in categories or 'comedy' in categories:
            return [(255, 215, 0), (255, 165, 0)]  # Золотой к оранжевому
        elif 'фантастика' in categories or 'sci-fi' in categories:
            return [(0, 191, 255), (25, 25, 112)]  # Голубой к темно-синему
        elif 'драма' in categories or 'drama' in categories:
            return [(75, 0, 130), (25, 25, 112)]  # Индиго к темно-синему
        elif 'триллер' in categories or 'thriller' in categories:
            return [(128, 0, 128), (0, 0, 0)]  # Фиолетовый к черному
        else:
            return [(229, 9, 20), (131, 16, 16)]  # Netflix красный (по умолчанию)

    def create_enhanced_poster(self, film, width=400, height=600):
        """Создает улучшенный постер с градиентами и эффектами"""
        # Создаем изображение
        img = Image.new('RGB', (width, height), color='#000000')
        draw = ImageDraw.Draw(img)
        
        # Получаем цвета для жанра
        color1, color2 = self.get_genre_colors(film)
        
        # Создаем диагональный градиент
        for y in range(height):
            for x in range(width):
                # Диагональный градиент
                ratio = (x + y) / (width + height)
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                
                # Добавляем немного шума для текстуры
                noise = random.randint(-10, 10)
                r = max(0, min(255, r + noise))
                g = max(0, min(255, g + noise))
                b = max(0, min(255, b + noise))
                
                img.putpixel((x, y), (r, g, b))
        
        # Добавляем полупрозрачный слой для лучшей читаемости текста
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 100))
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Добавляем рамку
        border_color = (229, 9, 20)  # Netflix красный
        draw.rectangle([0, 0, width-1, height-1], outline=border_color, width=3)
        draw.rectangle([5, 5, width-6, height-6], outline=border_color, width=1)
        
        # Загружаем шрифты
        try:
            font_title = ImageFont.truetype("arial.ttf", 36)
            font_year = ImageFont.truetype("arial.ttf", 24)
            font_brand = ImageFont.truetype("arial.ttf", 18)
            font_rating = ImageFont.truetype("arial.ttf", 20)
        except:
            try:
                font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
                font_year = ImageFont.truetype("DejaVuSans.ttf", 24)
                font_brand = ImageFont.truetype("DejaVuSans.ttf", 18)
                font_rating = ImageFont.truetype("DejaVuSans.ttf", 20)
            except:
                font_title = ImageFont.load_default()
                font_year = ImageFont.load_default()
                font_brand = ImageFont.load_default()
                font_rating = ImageFont.load_default()
        
        # Разбиваем название на строки
        title = film.title
        words = title.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=font_title)
            if bbox[2] - bbox[0] <= width - 60:  # Отступ 30px с каждой стороны
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Рисуем название в центре
        total_text_height = len(lines) * 45
        start_y = (height - total_text_height) // 2 - 50
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font_title)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = start_y + i * 45
            
            # Тень для лучшей читаемости
            for offset in [(2, 2), (1, 1), (-1, -1), (-2, -2)]:
                draw.text((x + offset[0], y + offset[1]), line, font=font_title, fill='#000000')
            
            # Основной текст
            draw.text((x, y), line, font=font_title, fill='#ffffff')
        
        # Добавляем год выпуска
        year_text = str(film.year)
        bbox = draw.textbbox((0, 0), year_text, font=font_year)
        year_width = bbox[2] - bbox[0]
        year_x = (width - year_width) // 2
        year_y = start_y + len(lines) * 45 + 20
        
        # Тень для года
        draw.text((year_x + 2, year_y + 2), year_text, font=font_year, fill='#000000')
        draw.text((year_x, year_y), year_text, font=font_year, fill='#cccccc')
        
        # Добавляем рейтинг
        rating_text = f"★ {film.rating}"
        bbox = draw.textbbox((0, 0), rating_text, font=font_rating)
        rating_width = bbox[2] - bbox[0]
        rating_x = (width - rating_width) // 2
        rating_y = year_y + 35
        
        # Фон для рейтинга
        draw.rectangle([rating_x - 10, rating_y - 5, rating_x + rating_width + 10, rating_y + 25], 
                      fill=(229, 9, 20), outline=(255, 255, 255), width=1)
        draw.text((rating_x, rating_y), rating_text, font=font_rating, fill='#ffffff')
        
        # Добавляем категории внизу
        categories_text = " • ".join([cat.name for cat in film.categories.all()[:2]])
        if categories_text:
            bbox = draw.textbbox((0, 0), categories_text, font=font_brand)
            cat_width = bbox[2] - bbox[0]
            cat_x = (width - cat_width) // 2
            cat_y = height - 80
            
            draw.text((cat_x + 1, cat_y + 1), categories_text, font=font_brand, fill='#000000')
            draw.text((cat_x, cat_y), categories_text, font=font_brand, fill='#888888')
        
        # Добавляем "TochkaFilms" внизу
        brand_text = "TOCHKAFILMS"
        bbox = draw.textbbox((0, 0), brand_text, font=font_brand)
        brand_width = bbox[2] - bbox[0]
        brand_x = (width - brand_width) // 2
        brand_y = height - 40
        
        # Фон для бренда
        draw.rectangle([brand_x - 5, brand_y - 3, brand_x + brand_width + 5, brand_y + 20], 
                      fill=(0, 0, 0), outline=(229, 9, 20), width=1)
        draw.text((brand_x, brand_y), brand_text, font=font_brand, fill=(229, 9, 20))
        
        return img

    def handle(self, *args, **kwargs):
        films = Film.objects.all()
        
        self.stdout.write(f'Создание постеров для {films.count()} фильмов...\n')
        
        for film in films:
            try:
                # Удаляем старый постер если есть
                if film.poster:
                    old_path = film.poster.path
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                # Создаем новый постер
                poster_img = self.create_enhanced_poster(film)
                
                # Сохраняем в BytesIO
                img_io = io.BytesIO()
                poster_img.save(img_io, format='JPEG', quality=95)
                img_io.seek(0)
                
                # Создаем имя файла
                base_name = self.transliterate_filename(film.title)
                if not base_name:  # Если название только из цифр
                    base_name = f"film_{film.id}"
                filename = f"{base_name}_{film.year}.jpg"
                
                # Сохраняем в модель
                film.poster.save(
                    filename,
                    ContentFile(img_io.getvalue()),
                    save=True
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'✓ {film.title} ({film.year}) -> {filename}')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Ошибка для "{film.title}": {str(e)}')
                )

        self.stdout.write(f'\n🎨 Создание постеров завершено!')
        self.stdout.write('Проверить результат: python manage.py check_posters')