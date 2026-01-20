import os
from PIL import Image, ImageDraw, ImageFont
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from films.models import Film
import io


class Command(BaseCommand):
    help = 'Создание улучшенных постеров для серии Крик'

    def create_scream_poster(self, title, year, number):
        """Создает постер в стиле ужасов для фильма Крик"""
        # Размеры постера
        width, height = 400, 600
        
        # Создаем изображение с темным градиентом
        img = Image.new('RGB', (width, height), color='black')
        draw = ImageDraw.Draw(img)
        
        # Создаем градиент от черного к темно-красному
        for y in range(height):
            # Градиент от черного (0,0,0) к темно-красному (80,0,0)
            red_intensity = int((y / height) * 80)
            color = (red_intensity, 0, 0)
            draw.line([(0, y), (width, y)], fill=color)
        
        # Добавляем текстуру царапин
        for i in range(50):
            x1 = i * 8
            y1 = 0
            x2 = x1 + 100
            y2 = height
            draw.line([(x1, y1), (x2, y2)], fill=(120, 0, 0), width=1)
        
        # Рисуем большой номер фильма
        try:
            # Пытаемся использовать системный шрифт
            title_font = ImageFont.truetype("arial.ttf", 120)
            subtitle_font = ImageFont.truetype("arial.ttf", 40)
            year_font = ImageFont.truetype("arial.ttf", 30)
        except:
            # Если не найден, используем стандартный
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            year_font = ImageFont.load_default()
        
        # Рисуем номер фильма большими буквами
        if number > 1:
            number_text = str(number)
            # Получаем размеры текста
            bbox = draw.textbbox((0, 0), number_text, font=title_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Центрируем номер
            x = (width - text_width) // 2
            y = height // 3
            
            # Рисуем тень
            draw.text((x+3, y+3), number_text, font=title_font, fill=(50, 0, 0))
            # Рисуем основной текст
            draw.text((x, y), number_text, font=title_font, fill=(255, 255, 255))
        
        # Рисуем название "КРИК"
        main_title = "КРИК"
        bbox = draw.textbbox((0, 0), main_title, font=subtitle_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height // 2 + 50
        
        # Тень
        draw.text((x+2, y+2), main_title, font=subtitle_font, fill=(100, 0, 0))
        # Основной текст
        draw.text((x, y), main_title, font=subtitle_font, fill=(255, 255, 255))
        
        # Рисуем год
        year_text = f"({year})"
        bbox = draw.textbbox((0, 0), year_text, font=year_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height - 100
        
        draw.text((x+1, y+1), year_text, font=year_font, fill=(80, 0, 0))
        draw.text((x, y), year_text, font=year_font, fill=(200, 200, 200))
        
        # Добавляем декоративные элементы
        # Рисуем "кровавые" капли
        for i in range(10):
            x = 50 + i * 30
            y = 50 + (i % 3) * 20
            draw.ellipse([x, y, x+8, y+12], fill=(150, 0, 0))
        
        # Рисуем рамку
        draw.rectangle([5, 5, width-5, height-5], outline=(100, 0, 0), width=3)
        
        return img

    def handle(self, *args, **options):
        self.stdout.write("🔪 СОЗДАНИЕ УЛУЧШЕННЫХ ПОСТЕРОВ КРИК")
        self.stdout.write("=" * 50)
        
        # Данные фильмов серии Крик
        scream_films = [
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
                self.stdout.write(f"🎨 Создаю постер для '{title}'...")
                
                # Создаем постер
                poster_img = self.create_scream_poster(title, year, number)
                
                # Сохраняем в память
                img_io = io.BytesIO()
                poster_img.save(img_io, format='JPEG', quality=95)
                img_io.seek(0)
                
                # Создаем имя файла
                filename = f"scream_{number}_poster.jpg"
                
                # Сохраняем файл
                film.poster.save(
                    filename,
                    ContentFile(img_io.getvalue()),
                    save=True
                )
                
                self.stdout.write(self.style.SUCCESS(f"  ✅ Постер для '{title}' создан"))
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
            self.stdout.write(self.style.SUCCESS(f"\n🔪 ПОСТЕРЫ КРИК ОБНОВЛЕНЫ!"))
            self.stdout.write("🎨 Теперь у серии Крик красивые постеры в стиле ужасов")
            self.stdout.write("🌐 Откройте сайт чтобы увидеть результат")
        
        # Финальная статистика
        total_films = Film.objects.count()
        films_with_posters = Film.objects.exclude(poster='').count()
        
        self.stdout.write(f"\n📈 ФИНАЛЬНАЯ СТАТИСТИКА:")
        self.stdout.write(f"  📁 Всего фильмов: {total_films}")
        self.stdout.write(f"  🖼️ С постерами: {films_with_posters}")
        self.stdout.write(f"  📊 Покрытие: {(films_with_posters/total_films*100):.1f}%")
        
        self.stdout.write(self.style.SUCCESS(f"\n🎬 TOCHKAFILMS - ВСЕ ПОСТЕРЫ ГОТОВЫ!"))
        self.stdout.write("🖼️ Оригинальные постеры + стильные постеры Крик")
        self.stdout.write("🔪 Серия ужасов выглядит потрясающе!")