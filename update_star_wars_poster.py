import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from films.models import Film


class Command(BaseCommand):
    help = 'Обновление постера для фильма "Звездные войны: Новая надежда"'

    def handle(self, *args, **options):
        self.stdout.write("🌟 ОБНОВЛЕНИЕ ПОСТЕРА ЗВЕЗДНЫХ ВОЙН")
        self.stdout.write("=" * 50)
        
        # Новый URL постера
        poster_url = 'https://ir.ozone.ru/s3/multimedia-y/c1000/6174008410.jpg'
        
        try:
            # Ищем фильм
            film = Film.objects.get(title='Звездные войны: Новая надежда')
            self.stdout.write(f"📽️ Найден фильм: {film.title}")
            
            # Загружаем новый постер
            self.stdout.write("📥 Загружаю новый постер...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Referer': 'https://www.ozone.ru/',
            }
            
            response = requests.get(poster_url, timeout=30, headers=headers)
            response.raise_for_status()
            
            # Проверяем размер файла
            if len(response.content) < 1000:
                raise Exception("Файл слишком маленький")
            
            # Проверяем тип контента
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                self.stdout.write(f"⚠️ Content-Type: {content_type}")
            
            # Сохраняем постер
            filename = "star_wars_new_hope_ozone.jpg"
            film.poster.save(filename, ContentFile(response.content), save=True)
            
            self.stdout.write(self.style.SUCCESS("✅ ПОСТЕР УСПЕШНО ОБНОВЛЕН!"))
            self.stdout.write(f"📁 Файл: {filename}")
            self.stdout.write(f"📏 Размер: {len(response.content)} байт")
            self.stdout.write(f"🔗 URL: {film.poster.url}")
            
            # Проверяем результат
            film.refresh_from_db()
            if film.poster:
                self.stdout.write(self.style.SUCCESS("🌟 Постер сохранен в базе данных"))
                self.stdout.write(f"📂 Путь: {film.poster.name}")
            else:
                self.stdout.write(self.style.ERROR("❌ Ошибка сохранения в базе"))
                
        except Film.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Фильм "Звездные войны: Новая надежда" не найден'))
            self.stdout.write("📋 Доступные фильмы со 'Звездные':")
            for film in Film.objects.filter(title__icontains='Звездные'):
                self.stdout.write(f"  - {film.title}")
                
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"❌ Ошибка загрузки: {str(e)}"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Общая ошибка: {str(e)}"))
        
        self.stdout.write("\n🚀 Команда завершена!")