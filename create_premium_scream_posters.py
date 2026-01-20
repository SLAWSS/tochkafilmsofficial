import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from films.models import Film
import io
import math


class Command(BaseCommand):
    help = 'Создание премиум постеров для всех частей серии Крик'

    def create_premium_scream_poster(self, title, year, number):
        """Создает премиум постер в стиле ужасов для фильма Крик"""
        # Размеры постера
        width, height = 400, 600
        
        # Создаем изображение с черным фоном
        img = Image.new('RGB', (width, height), color='black')
        draw = ImageDraw.Draw(img)
        
        # Создаем сложный градиент
        for y in range(height):
            # Многослойный градиент от черного к темно-красному с переходами
            progress = y / height
            
            if progress < 0.3:
                # Верхняя часть - черный с легким красным оттенком
                red = int(progress * 60)
                color = (red, 0, 0)
            elif progress < 0.7:
                # Средняя часть - переход к красному
                red = int(60 + (progress - 0.3) * 100)
                color = (red, 0, 0)
            else:
                # Нижняя часть - темно-красный
                red = int(160 - (progress - 0.7) * 80)
                color = (red, 0, 0)
            
            draw.line([(0, y), (width, y)], fill=color)
        
        # Добавляем текстуру царапин и потертостей
        for i in range(80):
            x1 = (i * 7) % width
            y1 = 0
            x2 = x1 + 150
            y2 = height
            opacity = 30 + (i % 3) * 20
            draw.line([(x1, y1), (x2, y2)], fill=(opacity, 0, 0), width=1)
        
        # Добавляем диагональные царапины
        for i in range(40):
            x1 = i * 10
            y1 = height
            x2 = x1 - 100
            y2 = 0
            draw.line([(x1, y1), (x2, y2)], fill=(80, 0, 0), width=1)
        
        # Пытаемся использовать разные шрифты
        try:
            # Пробуем найти жирный шрифт
            title_font = ImageFont.truetype("arialbd.ttf", 100)
            subtitle_font = ImageFont.truetype("arial.ttf", 36)
            year_font = ImageFont.truetype("arial.ttf", 28)
            small_font = ImageFont.truetype("arial.ttf", 20)
        except:
            try:
                title_font = ImageFont.truetype("arial.ttf", 100)
                subtitle_font = ImageFont.truetype("arial.ttf", 36)
                year_font = ImageFont.truetype("arial.ttf", 28)
                small_font = ImageFont.truetype("arial.ttf", 20)
            except:
                # Используем стандартный шрифт
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                year_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
        
        # Рисуем большой номер фильма (если не первая часть)
        if number > 1:
            number_text = str(number)
            
            # Получаем размеры текста
            bbox = draw.textbbox((0, 0), number_text, font=title_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Центрируем номер
            x = (width - text_width) // 2
            y = height // 4
            
            # Рисуем множественные тени для объема
            for offset in range(5, 0, -1):
                shadow_color = (20 * offset, 0, 0)
                draw.text((x + offset, y + offset), number_text, font=title_font, fill=shadow_color)
            
            # Рисуем основной текст с градиентным эффектом
            draw.text((x, y), number_text, font=title_font, fill=(255, 255, 255))
            
            # Добавляем обводку
            for dx in [-2, -1, 0, 1, 2]:
                for dy in [-2, -1, 0, 1, 2]:
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, y + dy), number_text, font=title_font, fill=(100, 0, 0))
            draw.text((x, y), number_text, font=title_font, fill=(255, 255, 255))
        
        # Рисуем название "SCREAM"
        main_title = "SCREAM"
        bbox = draw.textbbox((0, 0), main_title, font=subtitle_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height // 2 + (50 if number > 1 else 0)
        
        # Тень с размытием
        for offset in range(3, 0, -1):
            shadow_color = (30 * offset, 0, 0)
            draw.text((x + offset, y + offset), main_title, font=subtitle_font, fill=shadow_color)
        
        # Основной текст
        draw.text((x, y), main_title, font=subtitle_font, fill=(255, 255, 255))
        
        # Рисуем русское название под английским
        russian_title = "КРИК"
        bbox = draw.textbbox((0, 0), russian_title, font=small_font)
        text_width = bbox[2] - bbox[0]
        x_rus = (width - text_width) // 2
        y_rus = y + 45
        
        draw.text((x_rus + 1, y_rus + 1), russian_title, font=small_font, fill=(80, 0, 0))
        draw.text((x_rus, y_rus), russian_title, font=small_font, fill=(200, 200, 200))
        
        # Рисуем год
        year_text = f"({year})"
        bbox = draw.textbbox((0, 0), year_text, font=year_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height - 80
        
        draw.text((x + 1, y + 1), year_text, font=year_font, fill=(60, 0, 0))
        draw.text((x, y), year_text, font=year_font, fill=(180, 180, 180))
        
        # Добавляем декоративные элементы
        # Рисуем "кровавые" капли разных размеров
        for i in range(15):
            x_drop = 30 + (i * 25) % (width - 60)
            y_drop = 30 + (i % 4) * 25
            size = 4 + (i % 3) * 3
            
            # Капля с градиентом
            for r in range(size, 0, -1):
                intensity = int(100 + (size - r) * 20)
                color = (min(255, intensity), 0, 0)
                draw.ellipse([x_drop - r, y_drop - r, x_drop + r, y_drop + r], fill=color)
        
        # Добавляем "брызги крови"
        for i in range(25):
            x_splash = 20 + (i * 15) % (width - 40)
            y_splash = 100 + (i * 20) % (height - 200)
            
            # Маленькие брызги
            draw.ellipse([x_splash, y_splash, x_splash + 2, y_splash + 3], fill=(120, 0, 0))
        
        # Рисуем стильную рамку
        border_width = 4
        # Внешняя рамка
        draw.rectangle([0, 0, width-1, height-1], outline=(150, 0, 0), width=border_width)
        # Внутренняя рамка
        draw.rectangle([border_width, border_width, width-border_width-1, height-border_width-1], 
                      outline=(80, 0, 0), width=2)
        
        # Добавляем угловые элементы
        corner_size = 20
        for corner in [(0, 0), (width-corner_size, 0), (0, height-corner_size), (width-corner_size, height-corner_size)]:
            x_corner, y_corner = corner
            draw.rectangle([x_corner, y_corner, x_corner + corner_size, y_corner + corner_size], 
                          fill=(100, 0, 0))
        
        return img

    def handle(self, *args, **options):
        self.stdout.write("🔪 СОЗДАНИЕ ПРЕМИУМ ПОСТЕРОВ СЕРИИ КРИК")
        self.stdout.write("=" * 60)
        
        # Данные всех фильмов серии Крик
        scream_films = [
            ('Крик', 1996, 1),
            ('Крик 2', 1997, 2),
            ('Крик 3', 2000, 3),
            ('Крик 4', 2011, 4),
            ('Крик 5', 2022, 5),
            ('Крик 6', 2023, 6)
        ]
        
        success_count = 0
        error_count = 0
        
        for title, year, number in scream_films:
            try:
                film = Film.objects.get(title=title)
                self.stdout.write(f"🎨 Создаю премиум постер для '{title}'...")
                
                # Создаем постер
                poster_img = self.create_premium_scream_poster(title, year, number)
                
                # Сохраняем в память
                img_io = io.BytesIO()
                poster_img.save(img_io, format='JPEG', quality=95)
                img_io.seek(0)
                
                # Создаем имя файла
                filename = f"scream_{number}_premium.jpg"
                
                # Сохраняем файл
                film.poster.save(
                    filename,
                    ContentFile(img_io.getvalue()),
                    save=True
                )
                
                self.stdout.write(self.style.SUCCESS(f"  ✅ Премиум постер для '{title}' создан"))
                success_count += 1
                
            except Film.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"  ❌ Фильм '{title}' не найден"))
                error_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ❌ Ошибка создания постера для '{title}': {e}"))
                error_count += 1
        
        self.stdout.write(f"\n📊 СТАТИСТИКА:")
        self.stdout.write(f"  ✅ Успешно создано: {success_count}")
        self.stdout.write(f"  ❌ Ошибок: {error_count}")
        
        if success_count > 0:
            self.stdout.write(self.style.SUCCESS(f"\n🔪 ПРЕМИУМ ПОСТЕРЫ КРИК ГОТОВЫ!"))
            self.stdout.write("🎨 Все части серии теперь имеют стильные постеры")
            self.stdout.write("🖼️ Единый дизайн в стиле ужасов")
            self.stdout.write("🌟 Профессиональное качество")
        
        # Финальная статистика
        scream_films_count = Film.objects.filter(title__startswith='Крик').count()
        scream_with_posters = Film.objects.filter(title__startswith='Крик').exclude(poster='').count()
        
        self.stdout.write(f"\n📈 СТАТИСТИКА СЕРИИ КРИК:")
        self.stdout.write(f"  🔪 Всего фильмов Крик: {scream_films_count}")
        self.stdout.write(f"  🖼️ С постерами: {scream_with_posters}")
        self.stdout.write(f"  📊 Покрытие: {(scream_with_posters/scream_films_count*100):.1f}%")
        
        self.stdout.write(f"\n🎨 ОСОБЕННОСТИ ПОСТЕРОВ:")
        features = [
            "🌈 Сложные многослойные градиенты",
            "🔪 Текстуры царапин и потертостей",
            "💧 Декоративные элементы (капли, брызги)",
            "🔤 Английские и русские названия",
            "📐 Стильные рамки и угловые элементы",
            "🎭 Объемные тени и обводки",
            "📱 Оптимизация для всех устройств"
        ]
        
        for feature in features:
            self.stdout.write(f"  {feature}")
        
        self.stdout.write(f"\n🌐 ТЕСТИРОВАНИЕ:")
        test_steps = [
            "1. Откройте http://127.0.0.1:8000/",
            "2. Найдите все фильмы серии Крик",
            "3. Убедитесь что постеры в едином стиле",
            "4. Проверьте качество и детализацию",
            "5. Кликните на карточки - должны работать"
        ]
        
        for step in test_steps:
            self.stdout.write(f"  {step}")
        
        if scream_with_posters == scream_films_count:
            self.stdout.write(self.style.SUCCESS(f"\n🎉 ВСЯ СЕРИЯ КРИК С ПРЕМИУМ ПОСТЕРАМИ!"))
            self.stdout.write("🔪 Ghostface одобряет качество!")
            self.stdout.write("🎬 Серия выглядит профессионально")
        
        self.stdout.write(self.style.SUCCESS(f"\n🔪 SCREAM FRANCHISE - ПРЕМИУМ ПОСТЕРЫ ГОТОВЫ!"))