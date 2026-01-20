import os
from PIL import Image, ImageDraw, ImageFont
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from films.models import Film
from django.conf import settings
import io


class Command(BaseCommand):
    help = 'Создает постеры-заглушки для фильмов'

    def create_poster(self, title, width=300, height=450):
        """Создает постер с названием фильма"""
        # Создаем изображение с градиентом
        img = Image.new('RGB', (width, height), color='#1a1a1a')
        draw = ImageDraw.Draw(img)
        
        # Создаем градиент
        for y in range(height):
            color_value = int(26 + (y / height) * 50)  # От темного к светлому
            color = (color_value, color_value, color_value)
            draw.line([(0, y), (width, y)], fill=color)
        
        # Добавляем красную полосу сверху (в стиле Netflix)
        draw.rectangle([0, 0, width, 20], fill='#e50914')
        
        # Пытаемся использовать системный шрифт
        try:
            font_large = ImageFont.truetype("arial.ttf", 24)
            font_small = ImageFont.truetype("arial.ttf", 16)
        except:
            try:
                font_large = ImageFont.truetype("DejaVuSans.ttf", 24)
                font_small = ImageFont.truetype("DejaVuSans.ttf", 16)
            except:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
        
        # Разбиваем длинное название на строки
        words = title.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=font_large)
            if bbox[2] - bbox[0] <= width - 40:  # Отступ 20px с каждой стороны
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Вычисляем позицию для центрирования текста
        total_height = len(lines) * 30
        start_y = (height - total_height) // 2
        
        # Рисуем название
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font_large)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = start_y + i * 30
            
            # Тень
            draw.text((x + 2, y + 2), line, font=font_large, fill='#000000')
            # Основной текст
            draw.text((x, y), line, font=font_large, fill='#ffffff')
        
        # Добавляем "TochkaFilms" внизу
        brand_text = "TochkaFilms"
        bbox = draw.textbbox((0, 0), brand_text, font=font_small)
        brand_width = bbox[2] - bbox[0]
        brand_x = (width - brand_width) // 2
        brand_y = height - 40
        
        draw.text((brand_x + 1, brand_y + 1), brand_text, font=font_small, fill='#000000')
        draw.text((brand_x, brand_y), brand_text, font=font_small, fill='#e50914')
        
        return img

    def handle(self, *args, **kwargs):
        films = Film.objects.all()
        
        for film in films:
            if film.poster:
                self.stdout.write(f'Постер для "{film.title}" уже существует')
                continue
            
            try:
                # Создаем постер
                poster_img = self.create_poster(film.title)
                
                # Сохраняем в BytesIO
                img_io = io.BytesIO()
                poster_img.save(img_io, format='JPEG', quality=85)
                img_io.seek(0)
                
                # Создаем имя файла
                filename = f"{film.title.lower().replace(' ', '_').replace('ё', 'e')}.jpg"
                
                # Сохраняем в модель
                film.poster.save(
                    filename,
                    ContentFile(img_io.getvalue()),
                    save=True
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'Постер для "{film.title}" создан успешно')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Ошибка при создании постера для "{film.title}": {str(e)}')
                )

        self.stdout.write(self.style.SUCCESS('Создание постеров завершено!'))