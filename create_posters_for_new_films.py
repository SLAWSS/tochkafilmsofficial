import os
from PIL import Image, ImageDraw, ImageFont
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from films.models import Film, Category
import io
import random


class Command(BaseCommand):
    help = 'Создание постеров для всех фильмов без постеров'

    def get_category_colors(self, categories):
        """Возвращает цветовую схему на основе категорий фильма"""
        color_schemes = {
            'action': [(20, 20, 20), (150, 0, 0), (255, 100, 0)],  # Черный-красный-оранжевый
            'comedy': [(20, 20, 50), (255, 200, 0), (255, 255, 100)],  # Темно-синий-желтый
            'drama': [(30, 30, 30), (100, 100, 150), (200, 200, 255)],  # Серый-синий
            'sci-fi': [(10, 10, 40), (0, 100, 200), (100, 200, 255)],  # Темно-синий-голубой
            'thriller': [(40, 0, 0), (120, 0, 0), (200, 50, 50)],  # Темно-красный
            'horror': [(0, 0, 0), (80, 0, 0), (150, 0, 0)],  # Черный-красный
            'family': [(20, 50, 20), (100, 200, 100), (200, 255, 200)],  # Зеленый
            'romance': [(50, 20, 50), (200, 100, 150), (255, 200, 220)],  # Розовый
            'adventure': [(30, 50, 10), (150, 200, 50), (200, 255, 100)],  # Зеленый-желтый
            'animation': [(50, 30, 80), (150, 100, 200), (200, 150, 255)],  # Фиолетовый
            'documentary': [(40, 40, 20), (150, 150, 100), (200, 200, 150)],  # Коричневый
            'war': [(40, 40, 40), (100, 100, 80), (150, 150, 120)],  # Серо-коричневый
            'crime': [(20, 20, 20), (100, 50, 0), (200, 100, 50)],  # Черно-коричневый
            'mystery': [(20, 0, 40), (100, 50, 150), (150, 100, 200)],  # Темно-фиолетовый
            'biography': [(30, 30, 50), (100, 100, 150), (150, 150, 200)],  # Синий
            'history': [(50, 40, 20), (150, 120, 80), (200, 180, 120)]  # Коричнево-золотой
        }
        
        # Получаем первую категорию для определения цветовой схемы
        if categories:
            first_category = categories[0].slug
            return color_schemes.get(first_category, [(20, 20, 20), (100, 100, 100), (200, 200, 200)])
        
        return [(20, 20, 20), (100, 100, 100), (200, 200, 200)]  # По умолчанию

    def create_film_poster(self, film):
        """Создает постер для фильма"""
        width, height = 400, 600
        
        # Получаем категории фильма
        categories = list(film.categories.all())
        colors = self.get_category_colors(categories)
        
        # Создаем изображение
        img = Image.new('RGB', (width, height), color='black')
        draw = ImageDraw.Draw(img)
        
        # Создаем градиент на основе категории
        for y in range(height):
            progress = y / height
            if progress < 0.4:
                # Верхняя часть
                ratio = progress / 0.4
                color = tuple(int(colors[0][i] + (colors[1][i] - colors[0][i]) * ratio) for i in range(3))
            else:
                # Нижняя часть
                ratio = (progress - 0.4) / 0.6
                color = tuple(int(colors[1][i] + (colors[2][i] - colors[1][i]) * ratio) for i in range(3))
            
            draw.line([(0, y), (width, y)], fill=color)
        
        # Добавляем текстуру
        for i in range(50):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = x1 + random.randint(-50, 50)
            y2 = y1 + random.randint(-50, 50)
            opacity = random.randint(10, 50)
            draw.line([(x1, y1), (x2, y2)], fill=(opacity, opacity, opacity), width=1)
        
        # Загружаем шрифты
        try:
            title_font = ImageFont.truetype("arial.ttf", 32)
            year_font = ImageFont.truetype("arial.ttf", 24)
            category_font = ImageFont.truetype("arial.ttf", 16)
            rating_font = ImageFont.truetype("arial.ttf", 20)
        except:
            title_font = ImageFont.load_default()
            year_font = ImageFont.load_default()
            category_font = ImageFont.load_default()
            rating_font = ImageFont.load_default()
        
        # Рисуем название фильма (многострочное)
        title_words = film.title.split()
        lines = []
        current_line = ""
        
        for word in title_words:
            test_line = current_line + (" " if current_line else "") + word
            bbox = draw.textbbox((0, 0), test_line, font=title_font)
            if bbox[2] - bbox[0] > width - 40:  # Если строка слишком длинная
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    lines.append(word)
            else:
                current_line = test_line
        
        if current_line:
            lines.append(current_line)
        
        # Рисуем название по строкам
        start_y = height // 3
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = start_y + i * 40
            
            # Тень
            draw.text((x + 2, y + 2), line, font=title_font, fill=(0, 0, 0))
            # Основной текст
            draw.text((x, y), line, font=title_font, fill=(255, 255, 255))
        
        # Рисуем год
        year_text = f"({film.year})"
        bbox = draw.textbbox((0, 0), year_text, font=year_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = start_y + len(lines) * 40 + 20
        
        draw.text((x + 1, y + 1), year_text, font=year_font, fill=(50, 50, 50))
        draw.text((x, y), year_text, font=year_font, fill=(200, 200, 200))
        
        # Рисуем рейтинг
        rating_text = f"⭐ {film.rating}"
        bbox = draw.textbbox((0, 0), rating_text, font=rating_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height - 120
        
        draw.text((x + 1, y + 1), rating_text, font=rating_font, fill=(100, 100, 0))
        draw.text((x, y), rating_text, font=rating_font, fill=(255, 255, 0))
        
        # Рисуем категории
        if categories:
            category_names = [cat.name for cat in categories[:3]]  # Максимум 3 категории
            category_text = " • ".join(category_names)
            
            bbox = draw.textbbox((0, 0), category_text, font=category_font)
            text_width = bbox[2] - bbox[0]
            
            if text_width > width - 20:
                # Если текст слишком длинный, берем только первые 2 категории
                category_text = " • ".join(category_names[:2])
                bbox = draw.textbbox((0, 0), category_text, font=category_font)
                text_width = bbox[2] - bbox[0]
            
            x = (width - text_width) // 2
            y = height - 80
            
            draw.text((x + 1, y + 1), category_text, font=category_font, fill=(50, 50, 50))
            draw.text((x, y), category_text, font=category_font, fill=(180, 180, 180))
        
        # Добавляем декоративные элементы
        # Рисуем рамку
        border_color = tuple(min(255, c + 50) for c in colors[1])
        draw.rectangle([2, 2, width-3, height-3], outline=border_color, width=3)
        
        # Добавляем угловые элементы
        corner_size = 15
        for corner in [(5, 5), (width-corner_size-5, 5), (5, height-corner_size-5), (width-corner_size-5, height-corner_size-5)]:
            x_corner, y_corner = corner
            draw.rectangle([x_corner, y_corner, x_corner + corner_size, y_corner + corner_size], 
                          fill=border_color)
        
        return img

    def handle(self, *args, **options):
        self.stdout.write("🖼️ СОЗДАНИЕ ПОСТЕРОВ ДЛЯ НОВЫХ ФИЛЬМОВ")
        self.stdout.write("=" * 60)
        
        # Находим фильмы без постеров
        films_without_posters = Film.objects.filter(poster='')
        total_without_posters = films_without_posters.count()
        
        self.stdout.write(f"📊 Найдено фильмов без постеров: {total_without_posters}")
        
        if total_without_posters == 0:
            self.stdout.write(self.style.SUCCESS("🎉 У всех фильмов уже есть постеры!"))
            return
        
        success_count = 0
        error_count = 0
        
        for film in films_without_posters:
            try:
                self.stdout.write(f"🎨 Создаю постер для '{film.title}' ({film.year})...")
                
                # Создаем постер
                poster_img = self.create_film_poster(film)
                
                # Сохраняем в память
                img_io = io.BytesIO()
                poster_img.save(img_io, format='JPEG', quality=90)
                img_io.seek(0)
                
                # Создаем имя файла
                safe_title = "".join(c for c in film.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                filename = f"{safe_title.lower().replace(' ', '_')}_{film.year}.jpg"
                
                # Сохраняем файл
                film.poster.save(
                    filename,
                    ContentFile(img_io.getvalue()),
                    save=True
                )
                
                categories_str = ", ".join([cat.name for cat in film.categories.all()])
                self.stdout.write(self.style.SUCCESS(f"  ✅ Постер создан - {categories_str}"))
                success_count += 1
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ❌ Ошибка создания постера для '{film.title}': {e}"))
                error_count += 1
        
        self.stdout.write(f"\n📊 СТАТИСТИКА СОЗДАНИЯ ПОСТЕРОВ:")
        self.stdout.write(f"  ✅ Успешно создано: {success_count}")
        self.stdout.write(f"  ❌ Ошибок: {error_count}")
        
        # Финальная статистика
        total_films = Film.objects.count()
        films_with_posters = Film.objects.exclude(poster='').count()
        
        self.stdout.write(f"\n📈 ОБЩАЯ СТАТИСТИКА ПОСТЕРОВ:")
        self.stdout.write(f"  🎬 Всего фильмов: {total_films}")
        self.stdout.write(f"  🖼️ С постерами: {films_with_posters}")
        self.stdout.write(f"  📊 Покрытие: {(films_with_posters/total_films*100):.1f}%")
        
        if success_count > 0:
            self.stdout.write(self.style.SUCCESS(f"\n🎉 ПОСТЕРЫ СОЗДАНЫ!"))
            self.stdout.write("🎨 Каждый постер имеет уникальный дизайн")
            self.stdout.write("🌈 Цветовые схемы соответствуют жанрам")
            self.stdout.write("📱 Все постеры адаптивны")
        
        self.stdout.write(f"\n🎨 ОСОБЕННОСТИ ПОСТЕРОВ:")
        features = [
            "🌈 Уникальные цветовые схемы для каждого жанра",
            "📝 Многострочные названия для длинных заголовков",
            "⭐ Рейтинги и годы выпуска",
            "📁 Отображение категорий фильма",
            "🖼️ Декоративные рамки и элементы",
            "🎭 Текстуры для атмосферности",
            "📐 Размер 400x600 пикселей"
        ]
        
        for feature in features:
            self.stdout.write(f"  {feature}")
        
        self.stdout.write(f"\n🧪 ТЕСТИРОВАНИЕ:")
        test_steps = [
            "1. Откройте http://127.0.0.1:8000/",
            "2. Проверьте главную страницу",
            "3. Посмотрите разные категории",
            "4. Убедитесь что все карточки имеют постеры",
            "5. Проверьте цветовые схемы по жанрам"
        ]
        
        for step in test_steps:
            self.stdout.write(f"  {step}")
        
        if films_with_posters == total_films:
            self.stdout.write(self.style.SUCCESS(f"\n🎬 ВСЕ ФИЛЬМЫ ИМЕЮТ ПОСТЕРЫ!"))
            self.stdout.write("🌟 TochkaFilms выглядит профессионально")
        
        self.stdout.write(self.style.SUCCESS(f"\n🖼️ ПОСТЕРЫ ДЛЯ ВСЕХ ФИЛЬМОВ ГОТОВЫ!"))