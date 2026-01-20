from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from films.models import Film
from PIL import Image, ImageDraw, ImageFont
import io
import random


class Command(BaseCommand):
    help = 'Обновляет постеры для популярных фильмов'

    def add_arguments(self, parser):
        parser.add_argument('--film', type=str, help='Название конкретного фильма для обновления')

    def handle(self, *args, **options):
        if options['film']:
            self.update_single_film(options['film'])
        else:
            self.update_all_popular_films()

    def update_all_popular_films(self):
        """Обновляет постеры для всех популярных фильмов"""
        films_to_update = [
            'Космическая одиссея',
            'Коко',
            'Вверх',
            'Головоломка',
            'Рататуй'
        ]
        
        self.stdout.write("=" * 60)
        self.stdout.write("🎬 ОБНОВЛЕНИЕ ПОСТЕРОВ ПОПУЛЯРНЫХ ФИЛЬМОВ")
        self.stdout.write("=" * 60)
        
        updated_count = 0
        for film_name in films_to_update:
            if self.update_film_poster(film_name):
                updated_count += 1
        
        self.stdout.write("")
        self.stdout.write(f"✅ Обновлено постеров: {updated_count} из {len(films_to_update)}")

    def update_single_film(self, film_name):
        """Обновляет постер для одного фильма"""
        self.stdout.write(f"🎬 Обновление постера для: {film_name}")
        self.update_film_poster(film_name)

    def update_film_poster(self, film_name):
        """Обновляет постер для конкретного фильма"""
        try:
            # Ищем фильм в базе
            film = None
            search_terms = {
                'Космическая одиссея': ['космическая', 'одиссея', '2001'],
                'Коко': ['коко', 'coco'],
                'Вверх': ['вверх', 'up'],
                'Головоломка': ['головоломка', 'inside out'],
                'Рататуй': ['рататуй', 'ratatouille']
            }
            
            # Поиск фильма
            for term in search_terms.get(film_name, [film_name.lower()]):
                film = Film.objects.filter(title__icontains=term).first()
                if film:
                    break
            
            if not film:
                self.stdout.write(f"❌ Фильм '{film_name}' не найден в базе")
                return False

            self.stdout.write(f"🎬 Найден фильм: {film.title} ({film.year})")
            
            # Создаем постер в зависимости от фильма
            poster_content = self.create_poster_for_film(film_name, film)
            
            # Сохраняем постер
            poster_filename = f"{film_name.lower().replace(' ', '_')}_{film.year}_poster.jpg"
            film.poster.save(
                poster_filename,
                ContentFile(poster_content),
                save=True
            )
            
            self.stdout.write(f"✅ Постер обновлен: {film.poster.url}")
            return True
            
        except Exception as e:
            self.stdout.write(f"❌ Ошибка при обновлении {film_name}: {e}")
            return False

    def create_poster_for_film(self, film_name, film):
        """Создает постер для конкретного фильма"""
        if 'космическая' in film_name.lower() or 'одиссея' in film_name.lower():
            return self.create_space_odyssey_poster(film)
        elif 'коко' in film_name.lower():
            return self.create_coco_poster(film)
        elif 'вверх' in film_name.lower():
            return self.create_up_poster(film)
        elif 'головоломка' in film_name.lower():
            return self.create_inside_out_poster(film)
        elif 'рататуй' in film_name.lower():
            return self.create_ratatouille_poster(film)
        else:
            return self.create_generic_poster(film)

    def create_space_odyssey_poster(self, film):
        """Создает постер для Космической одиссеи"""
        width, height = 400, 600
        img = Image.new('RGB', (width, height), color='black')
        draw = ImageDraw.Draw(img)
        
        # Космический фон с звездами
        random.seed(42)
        for _ in range(200):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(1, 3)
            brightness = random.randint(100, 255)
            draw.ellipse([x-size, y-size, x+size, y+size], 
                        fill=(brightness, brightness, brightness))
        
        # Большая планета (Юпитер)
        planet_x, planet_y = width - 100, 150
        planet_radius = 80
        for r in range(planet_radius, 0, -2):
            color_intensity = int(255 * (r / planet_radius))
            color = (color_intensity // 2, color_intensity // 3, color_intensity // 4)
            draw.ellipse([
                planet_x - r, planet_y - r,
                planet_x + r, planet_y + r
            ], fill=color)
        
        # Космический корабль (простой)
        ship_x, ship_y = width // 2, height - 200
        draw.ellipse([ship_x - 30, ship_y - 10, ship_x + 30, ship_y + 10], 
                    fill=(200, 200, 200), outline=(150, 150, 150), width=2)
        
        # Название
        try:
            font_title = ImageFont.truetype("arial.ttf", 36)
            font_subtitle = ImageFont.truetype("arial.ttf", 20)
        except:
            font_title = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()
        
        title_text = "КОСМИЧЕСКАЯ"
        title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        
        draw.text((title_x + 2, 52), title_text, fill=(0, 0, 0), font=font_title)
        draw.text((title_x, 50), title_text, fill=(255, 255, 255), font=font_title)
        
        subtitle_text = "ОДИССЕЯ"
        subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=font_title)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        subtitle_x = (width - subtitle_width) // 2
        
        draw.text((subtitle_x + 2, 92), subtitle_text, fill=(0, 0, 0), font=font_title)
        draw.text((subtitle_x, 90), subtitle_text, fill=(255, 255, 255), font=font_title)
        
        return self.save_image_to_bytes(img)

    def create_coco_poster(self, film):
        """Создает постер для Коко"""
        width, height = 400, 600
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Мексиканский градиент (оранжевый к красному)
        for y in range(height):
            r = int(255 * (1 - y / height * 0.3))
            g = int(165 * (1 - y / height * 0.5))
            b = int(0 * (1 - y / height * 0.7))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Гитара (упрощенная)
        guitar_x, guitar_y = width // 2, height - 150
        # Корпус гитары
        draw.ellipse([guitar_x - 40, guitar_y - 60, guitar_x + 40, guitar_y + 60], 
                    fill=(139, 69, 19), outline=(101, 67, 33), width=3)
        # Гриф
        draw.rectangle([guitar_x - 8, guitar_y - 120, guitar_x + 8, guitar_y - 60], 
                      fill=(101, 67, 33), outline=(70, 50, 20), width=2)
        
        # Цветы (маригольды)
        flower_colors = [(255, 165, 0), (255, 140, 0), (255, 215, 0)]
        for i in range(15):
            x = random.randint(50, width - 50)
            y = random.randint(height - 100, height - 20)
            color = random.choice(flower_colors)
            size = random.randint(8, 15)
            draw.ellipse([x - size, y - size, x + size, y + size], fill=color)
        
        # Название
        try:
            font_title = ImageFont.truetype("arial.ttf", 60)
        except:
            font_title = ImageFont.load_default()
        
        title_text = "КОКО"
        title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        
        draw.text((title_x + 3, 53), title_text, fill=(0, 0, 0), font=font_title)
        draw.text((title_x, 50), title_text, fill=(255, 215, 0), font=font_title)
        
        return self.save_image_to_bytes(img)

    def create_up_poster(self, film):
        """Создает постер для Вверх"""
        width, height = 400, 600
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Небесный градиент
        for y in range(height):
            blue_intensity = int(135 + 120 * (y / height))
            color = (135, 206, blue_intensity)
            draw.line([(0, y), (width, y)], fill=color)
        
        # Облака
        cloud_color = (255, 255, 255, 180)
        for i in range(8):
            x = random.randint(0, width)
            y = random.randint(0, height // 2)
            size = random.randint(20, 40)
            draw.ellipse([x - size, y - size//2, x + size, y + size//2], 
                        fill=(255, 255, 255))
        
        # Дом с шариками
        house_x, house_y = width // 2, height - 200
        # Дом
        draw.rectangle([house_x - 30, house_y - 30, house_x + 30, house_y + 30], 
                      fill=(139, 69, 19), outline=(101, 67, 33), width=2)
        # Крыша
        draw.polygon([
            (house_x - 35, house_y - 30),
            (house_x, house_y - 60),
            (house_x + 35, house_y - 30)
        ], fill=(178, 34, 34))
        
        # Шарики
        balloon_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), 
                         (255, 0, 255), (0, 255, 255)]
        for i in range(20):
            x = house_x + random.randint(-60, 60)
            y = house_y - 80 - random.randint(0, 100)
            color = random.choice(balloon_colors)
            size = random.randint(8, 15)
            draw.ellipse([x - size, y - size, x + size, y + size], fill=color)
            # Ниточка
            draw.line([(x, y + size), (house_x, house_y - 60)], fill=(0, 0, 0), width=1)
        
        # Название
        try:
            font_title = ImageFont.truetype("arial.ttf", 60)
        except:
            font_title = ImageFont.load_default()
        
        title_text = "ВВЕРХ"
        title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        
        draw.text((title_x + 3, 53), title_text, fill=(0, 0, 0), font=font_title)
        draw.text((title_x, 50), title_text, fill=(255, 255, 255), font=font_title)
        
        return self.save_image_to_bytes(img)

    def create_inside_out_poster(self, film):
        """Создает постер для Головоломки"""
        width, height = 400, 600
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Радужный градиент
        colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255)]
        for y in range(height):
            color_index = int((y / height) * (len(colors) - 1))
            if color_index >= len(colors) - 1:
                color = colors[-1]
            else:
                # Интерполяция между цветами
                t = (y / height) * (len(colors) - 1) - color_index
                c1 = colors[color_index]
                c2 = colors[color_index + 1]
                color = (
                    int(c1[0] * (1 - t) + c2[0] * t),
                    int(c1[1] * (1 - t) + c2[1] * t),
                    int(c1[2] * (1 - t) + c2[2] * t)
                )
            draw.line([(0, y), (width, y)], fill=color)
        
        # Эмоции (цветные круги)
        emotions = [
            (width // 2 - 80, height // 2, (255, 255, 0)),  # Радость
            (width // 2 + 80, height // 2, (0, 0, 255)),    # Грусть
            (width // 2, height // 2 - 80, (255, 0, 0)),    # Гнев
            (width // 2 - 40, height // 2 + 80, (0, 255, 0)), # Брезгливость
            (width // 2 + 40, height // 2 + 80, (128, 0, 128)) # Страх
        ]
        
        for x, y, color in emotions:
            draw.ellipse([x - 25, y - 25, x + 25, y + 25], fill=color, outline=(0, 0, 0), width=3)
        
        # Название
        try:
            font_title = ImageFont.truetype("arial.ttf", 40)
        except:
            font_title = ImageFont.load_default()
        
        title_text = "ГОЛОВОЛОМКА"
        title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        
        draw.text((title_x + 2, 52), title_text, fill=(0, 0, 0), font=font_title)
        draw.text((title_x, 50), title_text, fill=(255, 255, 255), font=font_title)
        
        return self.save_image_to_bytes(img)

    def create_ratatouille_poster(self, film):
        """Создает постер для Рататуя"""
        width, height = 400, 600
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Парижский фон (теплые тона)
        for y in range(height):
            r = int(255 * (1 - y / height * 0.2))
            g = int(228 * (1 - y / height * 0.3))
            b = int(181 * (1 - y / height * 0.4))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Эйфелева башня (силуэт)
        tower_x = width - 80
        tower_base = height - 50
        draw.polygon([
            (tower_x - 30, tower_base),
            (tower_x + 30, tower_base),
            (tower_x + 15, tower_base - 100),
            (tower_x - 15, tower_base - 100)
        ], fill=(64, 64, 64))
        draw.polygon([
            (tower_x - 15, tower_base - 100),
            (tower_x + 15, tower_base - 100),
            (tower_x + 8, tower_base - 180),
            (tower_x - 8, tower_base - 180)
        ], fill=(64, 64, 64))
        
        # Крыса (упрощенная)
        rat_x, rat_y = width // 2 - 50, height - 150
        # Тело
        draw.ellipse([rat_x - 25, rat_y - 15, rat_x + 25, rat_y + 15], 
                    fill=(128, 128, 128), outline=(64, 64, 64), width=2)
        # Голова
        draw.ellipse([rat_x + 15, rat_y - 20, rat_x + 35, rat_y], 
                    fill=(128, 128, 128), outline=(64, 64, 64), width=2)
        # Уши
        draw.ellipse([rat_x + 20, rat_y - 25, rat_x + 25, rat_y - 15], fill=(255, 192, 203))
        draw.ellipse([rat_x + 25, rat_y - 25, rat_x + 30, rat_y - 15], fill=(255, 192, 203))
        # Хвост
        draw.arc([rat_x - 40, rat_y - 10, rat_x - 10, rat_y + 20], 0, 180, fill=(128, 128, 128), width=5)
        
        # Поварской колпак
        hat_x, hat_y = rat_x + 25, rat_y - 35
        draw.rectangle([hat_x - 8, hat_y, hat_x + 8, hat_y + 15], fill=(255, 255, 255))
        draw.ellipse([hat_x - 10, hat_y - 5, hat_x + 10, hat_y + 5], fill=(255, 255, 255))
        
        # Название
        try:
            font_title = ImageFont.truetype("arial.ttf", 48)
        except:
            font_title = ImageFont.load_default()
        
        title_text = "РАТАТУЙ"
        title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        
        draw.text((title_x + 2, 52), title_text, fill=(0, 0, 0), font=font_title)
        draw.text((title_x, 50), title_text, fill=(255, 215, 0), font=font_title)
        
        return self.save_image_to_bytes(img)

    def create_generic_poster(self, film):
        """Создает общий постер"""
        width, height = 400, 600
        img = Image.new('RGB', (width, height), color=(50, 50, 100))
        draw = ImageDraw.Draw(img)
        
        try:
            font_title = ImageFont.truetype("arial.ttf", 36)
        except:
            font_title = ImageFont.load_default()
        
        title_bbox = draw.textbbox((0, 0), film.title, font=font_title)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        
        draw.text((title_x, height // 2), film.title, fill=(255, 255, 255), font=font_title)
        
        return self.save_image_to_bytes(img)

    def save_image_to_bytes(self, img):
        """Сохраняет изображение в байты"""
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=95)
        return img_byte_arr.getvalue()