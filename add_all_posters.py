from django.core.management.base import BaseCommand
from films.models import Film
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont
import os
import tempfile


class Command(BaseCommand):
    help = 'Добавляет постеры всем фильмам без них'

    def handle(self, *args, **options):
        # Находим фильмы без постеров
        films_without_posters = []
        all_films = Film.objects.all()
        
        for film in all_films:
            if not film.poster:
                films_without_posters.append(film)
        
        if not films_without_posters:
            self.stdout.write("✅ Все фильмы уже имеют постеры!")
            return
        
        self.stdout.write(f"Найдено {len(films_without_posters)} фильмов без постеров:")
        
        for film in films_without_posters:
            self.stdout.write(f"- ID {film.id}: {film.title} ({film.year})")
        
        self.stdout.write("\nДобавляю постеры...")
        
        success_count = 0
        for film in films_without_posters:
            if self.create_and_add_poster(film):
                success_count += 1
        
        self.stdout.write(f"\n✅ Добавлено постеров: {success_count} из {len(films_without_posters)}")

    def create_and_add_poster(self, film):
        """Создает и добавляет постер к фильму"""
        try:
            # Создаем постер
            poster_img = self.create_poster(film.title, film.year)
            
            # Сохраняем во временный файл
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                poster_img.save(temp_file.name, 'JPEG', quality=85)
                temp_path = temp_file.name
            
            # Добавляем к фильму
            filename = f"{film.title.lower().replace(' ', '_').replace(':', '').replace('(', '').replace(')', '')}_poster.jpg"
            
            with open(temp_path, 'rb') as f:
                film.poster.save(filename, File(f))
            
            # Удаляем временный файл
            os.unlink(temp_path)
            
            self.stdout.write(f"✅ Постер создан для '{film.title}'")
            return True
            
        except Exception as e:
            self.stdout.write(f"❌ Ошибка создания постера для '{film.title}': {e}")
            return False

    def create_poster(self, title, year, width=300, height=450):
        """Создает красивый постер с названием фильма"""
        # Цветовые схемы для разных жанров
        color_schemes = [
            {'bg': '#1a1a2e', 'primary': '#16213e', 'text': '#e94560', 'subtitle': '#f5f5f5'},
            {'bg': '#0f3460', 'primary': '#16537e', 'text': '#e94560', 'subtitle': '#f5f5f5'},
            {'bg': '#533483', 'primary': '#7209b7', 'text': '#f72585', 'subtitle': '#f8f9fa'},
            {'bg': '#2d1b69', 'primary': '#11009e', 'text': '#4cc9f0', 'subtitle': '#f8f9fa'},
            {'bg': '#641220', 'primary': '#85182a', 'text': '#f71735', 'subtitle': '#f8f9fa'},
        ]
        
        # Выбираем цветовую схему на основе хеша названия
        scheme = color_schemes[hash(title) % len(color_schemes)]
        
        # Создаем изображение с градиентом
        img = Image.new('RGB', (width, height), color=scheme['bg'])
        draw = ImageDraw.Draw(img)
        
        # Создаем простой градиент
        for y in range(height):
            alpha = y / height
            r1, g1, b1 = tuple(int(scheme['bg'][i:i+2], 16) for i in (1, 3, 5))
            r2, g2, b2 = tuple(int(scheme['primary'][i:i+2], 16) for i in (1, 3, 5))
            
            r = int(r1 * (1 - alpha) + r2 * alpha)
            g = int(g1 * (1 - alpha) + g2 * alpha)
            b = int(b1 * (1 - alpha) + b2 * alpha)
            
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Загружаем шрифты
        try:
            title_font = ImageFont.truetype("arial.ttf", 28)
            year_font = ImageFont.truetype("arial.ttf", 20)
            label_font = ImageFont.truetype("arial.ttf", 16)
        except:
            title_font = ImageFont.load_default()
            year_font = ImageFont.load_default()
            label_font = ImageFont.load_default()
        
        # Добавляем декоративные элементы
        # Рамка
        draw.rectangle([(10, 10), (width-10, height-10)], outline=scheme['text'], width=2)
        
        # Верхняя метка "ФИЛЬМ"
        label_text = "ФИЛЬМ"
        bbox = draw.textbbox((0, 0), label_text, font=label_font)
        label_width = bbox[2] - bbox[0]
        label_x = (width - label_width) // 2
        draw.text((label_x, 30), label_text, fill=scheme['text'], font=label_font)
        
        # Разбиваем название на строки
        words = title.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=title_font)
            if bbox[2] - bbox[0] <= width - 60:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Рисуем название по центру
        total_text_height = len(lines) * 35
        start_y = (height - total_text_height) // 2
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=title_font)
            line_width = bbox[2] - bbox[0]
            line_x = (width - line_width) // 2
            line_y = start_y + i * 35
            
            # Тень для текста
            draw.text((line_x + 2, line_y + 2), line, fill='black', font=title_font)
            # Основной текст
            draw.text((line_x, line_y), line, fill=scheme['subtitle'], font=title_font)
        
        # Год внизу
        year_text = str(year)
        bbox = draw.textbbox((0, 0), year_text, font=year_font)
        year_width = bbox[2] - bbox[0]
        year_x = (width - year_width) // 2
        year_y = height - 60
        
        draw.text((year_x + 1, year_y + 1), year_text, fill='black', font=year_font)
        draw.text((year_x, year_y), year_text, fill=scheme['text'], font=year_font)
        
        # Декоративные линии
        draw.line([(30, year_y - 20), (width - 30, year_y - 20)], fill=scheme['text'], width=1)
        draw.line([(30, 70), (width - 30, 70)], fill=scheme['text'], width=1)
        
        return img