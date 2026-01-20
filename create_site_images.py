import os
from PIL import Image, ImageDraw, ImageFont
from django.core.management.base import BaseCommand
from django.conf import settings
import io


class Command(BaseCommand):
    help = 'Создает дополнительные изображения для сайта'

    def create_logo(self, width=200, height=60):
        """Создает логотип TochkaFilms"""
        img = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except:
            try:
                font = ImageFont.truetype("DejaVuSans-Bold.ttf", 32)
            except:
                font = ImageFont.load_default()
        
        text = "TochkaFilms"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Тень
        draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0, 128))
        # Основной текст
        draw.text((x, y), text, font=font, fill=(229, 9, 20, 255))
        
        return img

    def create_hero_background(self, width=1400, height=400):
        """Создает фоновое изображение для hero секции"""
        img = Image.new('RGB', (width, height), color='#141414')
        draw = ImageDraw.Draw(img)
        
        # Создаем градиент от красного к черному
        for y in range(height):
            red_value = int(229 * (1 - y / height))
            color = (red_value, int(red_value * 0.04), int(red_value * 0.08))
            draw.line([(0, y), (width, y)], fill=color)
        
        # Добавляем геометрические элементы
        for i in range(0, width, 100):
            alpha = int(50 * (1 - i / width))
            draw.line([(i, 0), (i + 200, height)], fill=(255, 255, 255, alpha), width=1)
        
        return img

    def create_category_icons(self):
        """Создает иконки для категорий"""
        categories = {
            'action': '⚡',
            'comedy': '😄', 
            'drama': '🎭',
            'sci-fi': '🚀',
            'thriller': '🔥',
            'horror': '👻'
        }
        
        icons = {}
        for category, emoji in categories.items():
            img = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Фон
            draw.ellipse([4, 4, 60, 60], fill=(229, 9, 20, 200))
            
            try:
                font = ImageFont.truetype("arial.ttf", 32)
            except:
                font = ImageFont.load_default()
            
            # Центрируем эмодзи
            bbox = draw.textbbox((0, 0), emoji, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (64 - text_width) // 2
            y = (64 - text_height) // 2
            
            draw.text((x, y), emoji, font=font, fill=(255, 255, 255, 255))
            icons[category] = img
        
        return icons

    def handle(self, *args, **kwargs):
        # Создаем папку для изображений сайта
        static_images_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
        os.makedirs(static_images_dir, exist_ok=True)
        
        try:
            # Создаем логотип
            logo = self.create_logo()
            logo_path = os.path.join(static_images_dir, 'logo.png')
            logo.save(logo_path, 'PNG')
            self.stdout.write(self.style.SUCCESS('Логотип создан'))
            
            # Создаем фоновое изображение
            hero_bg = self.create_hero_background()
            hero_path = os.path.join(static_images_dir, 'hero-bg.jpg')
            hero_bg.save(hero_path, 'JPEG', quality=85)
            self.stdout.write(self.style.SUCCESS('Фоновое изображение создано'))
            
            # Создаем иконки категорий
            category_icons = self.create_category_icons()
            for category, icon in category_icons.items():
                icon_path = os.path.join(static_images_dir, f'{category}-icon.png')
                icon.save(icon_path, 'PNG')
                self.stdout.write(self.style.SUCCESS(f'Иконка для {category} создана'))
            
            self.stdout.write(self.style.SUCCESS('Все изображения созданы успешно!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при создании изображений: {str(e)}'))