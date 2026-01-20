import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from films.models import Film


class Command(BaseCommand):
    help = 'Обновление постера для фильма "Джон Уик 2"'

    def handle(self, *args, **options):
        self.stdout.write("🔫 ОБНОВЛЕНИЕ ПОСТЕРА 'ДЖОН УИК 2'")
        self.stdout.write("=" * 45)
        
        # URL постера с КиноПоиск (Яндекс)
        poster_url = 'https://avatars.mds.yandex.net/get-kinopoisk-image/1777765/6c047c95-648d-477e-8ea0-33f625628788/orig'
        
        try:
            # Ищем фильм
            film = Film.objects.get(title='Джон Уик 2')
            self.stdout.write(f"🎬 Найден фильм: {film.title} ({film.year})")
            
            # Загружаем новый постер
            self.stdout.write("📥 Загружаю постер с КиноПоиск...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Referer': 'https://www.kinopoisk.ru/',
            }
            
            response = requests.get(poster_url, timeout=30, headers=headers)
            response.raise_for_status()
            
            # Проверяем размер файла
            if len(response.content) < 1000:
                raise Exception("Файл слишком маленький")
            
            # Проверяем тип контента
            content_type = response.headers.get('content-type', '')
            self.stdout.write(f"📄 Content-Type: {content_type}")
            
            # Сохраняем постер
            filename = "john_wick_2_2017_kinopoisk.jpg"
            film.poster.save(filename, ContentFile(response.content), save=True)
            
            self.stdout.write(self.style.SUCCESS("✅ ПОСТЕР УСПЕШНО ОБНОВЛЕН!"))
            self.stdout.write(f"📁 Файл: {filename}")
            self.stdout.write(f"📏 Размер: {len(response.content)} байт")
            self.stdout.write(f"🔗 URL: {film.poster.url}")
            self.stdout.write(f"📅 Год фильма: {film.year}")
            self.stdout.write(f"⭐ Рейтинг: {film.rating}")
            self.stdout.write(f"🎭 Главная роль: Киану Ривз")
            self.stdout.write(f"🎬 Режиссер: Чад Стахелски")
            self.stdout.write(f"🔫 Легендарный киллер")
            
            # Проверяем результат
            film.refresh_from_db()
            if film.poster:
                self.stdout.write(self.style.SUCCESS("🔫 Постер сохранен в базе данных"))
                self.stdout.write(f"📂 Путь: {film.poster.name}")
                
                # Показываем категории
                categories = film.categories.all()
                if categories:
                    self.stdout.write(f"🎭 Категории: {', '.join([cat.name for cat in categories])}")
                    
                # Проверяем файл
                try:
                    with film.poster.open('rb') as f:
                        header = f.read(12)
                        if header.startswith(b'\xff\xd8\xff'):
                            self.stdout.write(self.style.SUCCESS("✅ Корректный JPEG файл"))
                        elif header.startswith(b'\x89PNG'):
                            self.stdout.write(self.style.SUCCESS("✅ Корректный PNG файл"))
                        elif header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
                            self.stdout.write(self.style.SUCCESS("✅ Корректный GIF файл"))
                        elif header.startswith(b'RIFF') and b'WEBP' in header:
                            self.stdout.write(self.style.SUCCESS("✅ Корректный WebP файл"))
                        else:
                            self.stdout.write(f"📄 Заголовок файла: {header.hex()}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"❌ Ошибка проверки: {e}"))
                    
            else:
                self.stdout.write(self.style.ERROR("❌ Ошибка сохранения в базе"))
                
        except Film.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Фильм "Джон Уик 2" не найден'))
            self.stdout.write("📋 Поиск похожих фильмов:")
            for film in Film.objects.filter(title__icontains='джон уик'):
                self.stdout.write(f"  - {film.title} ({film.year})")
            for film in Film.objects.filter(title__icontains='john wick'):
                self.stdout.write(f"  - {film.title} ({film.year})")
                
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"❌ Ошибка загрузки: {str(e)}"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Общая ошибка: {str(e)}"))
        
        self.stdout.write("\n🔫 Команда завершена!")