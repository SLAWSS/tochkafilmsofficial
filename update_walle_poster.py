from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from films.models import Film
import requests
from PIL import Image, ImageDraw, ImageFont
import io


class Command(BaseCommand):
    help = 'Обновляет постер для фильма ВАЛЛ-И'

    def handle(self, *args, **options):
        self.update_walle_poster()

    def update_walle_poster(self):
        """Обновляет постер ВАЛЛ-И"""
        try:
            # Ищем фильм ВАЛЛ-И
            film = Film.objects.filter(title__icontains='ВАЛЛ').first()
            if not film:
                self.stdout.write("❌ Фильм ВАЛЛ-И не найден")
                return

            self.stdout.write(f"🎬 Найден фильм: {film.title} ({film.year})")
            
            # Создаем красивый постер для ВАЛЛ-И
            poster_content = self.create_walle_poster()
            
            # Сохраняем постер
            poster_filename = f"walle_{film.year}_poster.jpg"
            film.poster.save(
                poster_filename,
                ContentFile(poster_content),
                save=True
            )
            
            self.stdout.write(f"✅ Постер обновлен: {film.poster.url}")
            
            # Показываем информацию о фильме
            self.show_film_info(film)
            
        except Exception as e:
            self.stdout.write(f"❌ Ошибка: {e}")

    def create_walle_poster(self):
        """Создает красивый постер для ВАЛЛ-И"""
        # Размеры постера
        width, height = 400, 600
        
        # Создаем изображение с космическим градиентом
        img = Image.new('RGB', (width, height), color='black')
        draw = ImageDraw.Draw(img)
        
        # Космический градиент (от темно-синего к черному)
        for y in range(height):
            # Градиент от темно-синего вверху к черному внизу
            blue_intensity = int(50 * (1 - y / height))
            color = (blue_intensity // 3, blue_intensity // 2, blue_intensity)
            draw.line([(0, y), (width, y)], fill=color)
        
        # Добавляем звезды
        import random
        random.seed(42)  # Для воспроизводимости
        for _ in range(100):
            x = random.randint(0, width)
            y = random.randint(0, height // 2)  # Звезды в верхней части
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            draw.ellipse([x-size, y-size, x+size, y+size], 
                        fill=(brightness, brightness, brightness))
        
        # Рисуем силуэт ВАЛЛ-И (упрощенный)
        # Корпус
        robot_x = width // 2
        robot_y = height - 200
        
        # Основной корпус (прямоугольник)
        body_width, body_height = 80, 60
        draw.rectangle([
            robot_x - body_width//2, robot_y - body_height//2,
            robot_x + body_width//2, robot_y + body_height//2
        ], fill=(139, 69, 19), outline=(101, 67, 33), width=2)
        
        # Гусеницы
        track_width, track_height = 90, 20
        draw.rectangle([
            robot_x - track_width//2, robot_y + 20,
            robot_x + track_width//2, robot_y + 20 + track_height
        ], fill=(64, 64, 64), outline=(32, 32, 32), width=2)
        
        # Глаза (бинокль)
        eye_size = 12
        eye_y = robot_y - 20
        # Левый глаз
        draw.ellipse([
            robot_x - 25 - eye_size, eye_y - eye_size,
            robot_x - 25 + eye_size, eye_y + eye_size
        ], fill=(100, 149, 237), outline=(70, 130, 180), width=2)
        # Правый глаз
        draw.ellipse([
            robot_x + 25 - eye_size, eye_y - eye_size,
            robot_x + 25 + eye_size, eye_y + eye_size
        ], fill=(100, 149, 237), outline=(70, 130, 180), width=2)
        
        # Руки (простые линии)
        arm_length = 40
        draw.line([
            robot_x - body_width//2, robot_y,
            robot_x - body_width//2 - arm_length, robot_y - 10
        ], fill=(139, 69, 19), width=8)
        draw.line([
            robot_x + body_width//2, robot_y,
            robot_x + body_width//2 + arm_length, robot_y - 10
        ], fill=(139, 69, 19), width=8)
        
        # Добавляем Землю внизу (коричневая поверхность)
        earth_y = height - 100
        for y in range(earth_y, height):
            brown_intensity = int(139 * (1 - (y - earth_y) / (height - earth_y)))
            color = (brown_intensity, brown_intensity // 2, brown_intensity // 4)
            draw.line([(0, y), (width, y)], fill=color)
        
        # Добавляем мусор на поверхности
        for i in range(20):
            x = random.randint(0, width)
            y = random.randint(earth_y, height - 20)
            size = random.randint(3, 8)
            color = (random.randint(60, 120), random.randint(60, 120), random.randint(60, 120))
            draw.rectangle([x, y, x + size, y + size], fill=color)
        
        # Добавляем название фильма
        try:
            # Пытаемся использовать системный шрифт
            font_title = ImageFont.truetype("arial.ttf", 48)
            font_subtitle = ImageFont.truetype("arial.ttf", 24)
        except:
            # Если не найден, используем стандартный
            font_title = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()
        
        # Название "ВАЛЛ-И"
        title_text = "ВАЛЛ-И"
        title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        
        # Тень для текста
        draw.text((title_x + 2, 52), title_text, fill=(0, 0, 0), font=font_title)
        # Основной текст
        draw.text((title_x, 50), title_text, fill=(255, 215, 0), font=font_title)
        
        # Подзаголовок
        subtitle_text = "WALL-E"
        subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=font_subtitle)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        subtitle_x = (width - subtitle_width) // 2
        
        # Тень для подзаголовка
        draw.text((subtitle_x + 1, 102), subtitle_text, fill=(0, 0, 0), font=font_subtitle)
        # Основной подзаголовок
        draw.text((subtitle_x, 100), subtitle_text, fill=(200, 200, 200), font=font_subtitle)
        
        # Год выпуска
        year_text = "2008"
        year_bbox = draw.textbbox((0, 0), year_text, font=font_subtitle)
        year_width = year_bbox[2] - year_bbox[0]
        year_x = (width - year_width) // 2
        
        draw.text((year_x + 1, 132), year_text, fill=(0, 0, 0), font=font_subtitle)
        draw.text((year_x, 130), year_text, fill=(255, 215, 0), font=font_subtitle)
        
        # Добавляем рамку
        draw.rectangle([0, 0, width-1, height-1], outline=(100, 100, 100), width=3)
        
        # Сохраняем в байты
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=95)
        return img_byte_arr.getvalue()

    def show_film_info(self, film):
        """Показывает информацию о фильме"""
        self.stdout.write("")
        self.stdout.write("=" * 50)
        self.stdout.write(f"🎬 ИНФОРМАЦИЯ О ФИЛЬМЕ")
        self.stdout.write("=" * 50)
        self.stdout.write(f"📽️  Название: {film.title}")
        self.stdout.write(f"📅 Год: {film.year}")
        self.stdout.write(f"⭐ Рейтинг: {film.rating}")
        self.stdout.write(f"⏱️  Длительность: {film.duration} мин")
        self.stdout.write(f"🖼️  Постер: {film.poster.url if film.poster else 'Нет'}")
        self.stdout.write(f"🎬 Трейлер: {'Есть' if film.trailer_url else 'Нет'}")
        
        # Категории
        categories = list(film.categories.all())
        if categories:
            cat_names = [cat.name for cat in categories]
            self.stdout.write(f"📁 Категории: {', '.join(cat_names)}")
        
        # Актеры
        actors = list(film.actors.all())
        if actors:
            actor_names = [actor.name for actor in actors]
            self.stdout.write(f"🎭 Актеры: {', '.join(actor_names)}")
        
        self.stdout.write("")
        self.stdout.write("📝 Описание:")
        self.stdout.write(f"   {film.description}")