from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Проверка постера Звездных войн'

    def handle(self, *args, **options):
        self.stdout.write("🌟 ПРОВЕРКА ПОСТЕРА ЗВЕЗДНЫХ ВОЙН")
        self.stdout.write("=" * 45)
        
        try:
            film = Film.objects.get(title='Звездные войны: Новая надежда')
            
            self.stdout.write(f"📽️ Фильм: {film.title}")
            self.stdout.write(f"📅 Год: {film.year}")
            self.stdout.write(f"⭐ Рейтинг: {film.rating}")
            
            if film.poster:
                self.stdout.write(self.style.SUCCESS("✅ ПОСТЕР НАЙДЕН!"))
                self.stdout.write(f"📂 Путь: {film.poster.name}")
                self.stdout.write(f"🔗 URL: {film.poster.url}")
                self.stdout.write(f"📏 Размер файла: {film.poster.size} байт")
                
                # Проверяем, что файл существует
                try:
                    with film.poster.open('rb') as f:
                        content = f.read(100)  # Читаем первые 100 байт
                        self.stdout.write(f"📄 Первые байты: {content[:20].hex()}")
                        
                        # Проверяем JPEG заголовок
                        if content.startswith(b'\xff\xd8\xff'):
                            self.stdout.write(self.style.SUCCESS("✅ Файл является корректным JPEG"))
                        else:
                            self.stdout.write(self.style.WARNING("⚠️ Файл может быть поврежден"))
                            
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"❌ Ошибка чтения файла: {e}"))
                    
            else:
                self.stdout.write(self.style.ERROR("❌ ПОСТЕР НЕ НАЙДЕН"))
                
            # Показываем категории
            categories = film.categories.all()
            if categories:
                self.stdout.write(f"🎭 Категории: {', '.join([cat.name for cat in categories])}")
                
            # Показываем трейлер
            if film.trailer_url:
                self.stdout.write(f"🎬 Трейлер: {film.trailer_url[:50]}...")
            else:
                self.stdout.write("🎬 Трейлер: не указан")
                
        except Film.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Фильм не найден'))
            
        self.stdout.write("\n🚀 Проверка завершена!")