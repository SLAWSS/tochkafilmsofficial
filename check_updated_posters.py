from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Проверка обновленных постеров'

    def handle(self, *args, **options):
        self.stdout.write("🖼️ ПРОВЕРКА ОБНОВЛЕННЫХ ПОСТЕРОВ")
        self.stdout.write("=" * 50)
        
        films_to_check = [
            'Звездные войны: Новая надежда',
            'Пианист',
            'Окно во двор',
            'Чужие',
            'Головокружение',
            'Крепкий орешек',
            'Игры разума',
            'Шестое чувство'
        ]
        
        for title in films_to_check:
            try:
                film = Film.objects.get(title=title)
                
                self.stdout.write(f"\n🎬 {film.title} ({film.year})")
                self.stdout.write("-" * 40)
                
                if film.poster:
                    self.stdout.write(self.style.SUCCESS("✅ Постер найден"))
                    self.stdout.write(f"📂 Файл: {film.poster.name}")
                    self.stdout.write(f"🔗 URL: {film.poster.url}")
                    self.stdout.write(f"📏 Размер: {film.poster.size} байт")
                    
                    # Проверяем формат файла
                    try:
                        with film.poster.open('rb') as f:
                            header = f.read(12)
                            if header.startswith(b'\xff\xd8\xff'):
                                self.stdout.write(self.style.SUCCESS("✅ Корректный JPEG"))
                            elif header.startswith(b'\x89PNG'):
                                self.stdout.write(self.style.SUCCESS("✅ Корректный PNG"))
                            elif header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
                                self.stdout.write(self.style.SUCCESS("✅ Корректный GIF"))
                            elif header.startswith(b'RIFF') and b'WEBP' in header:
                                self.stdout.write(self.style.SUCCESS("✅ Корректный WebP"))
                            else:
                                self.stdout.write(self.style.WARNING("⚠️ Неизвестный формат"))
                    except:
                        self.stdout.write(self.style.ERROR("❌ Ошибка чтения"))
                        
                else:
                    self.stdout.write(self.style.ERROR("❌ Постер отсутствует"))
                    
                # Показываем дополнительную информацию
                self.stdout.write(f"⭐ Рейтинг: {film.rating}")
                categories = film.categories.all()
                if categories:
                    self.stdout.write(f"🎭 Категории: {', '.join([cat.name for cat in categories])}")
                    
            except Film.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Фильм "{title}" не найден'))
        
        self.stdout.write(f"\n🚀 Проверка завершена!")