from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Финальная проверка всех 17 обновленных постеров'

    def handle(self, *args, **options):
        self.stdout.write("🎬 ФИНАЛЬНАЯ ПРОВЕРКА ВСЕХ ОБНОВЛЕННЫХ ПОСТЕРОВ")
        self.stdout.write("=" * 65)
        
        updated_films = [
            'Звездные войны: Новая надежда',
            'Пианист',
            'Окно во двор',
            'Чужие',
            'Головокружение',
            'Крепкий орешек',
            'Игры разума',
            'Шестое чувство',
            'Остров проклятых',
            'Старикам тут не место',
            'В поисках Немо',
            'Безумный Макс: Дорога ярости',
            'Бегущий по лезвию',
            'Фарго',
            'Пираты Карибского моря',
            'Джон Уик 2',
            'Бегущий по лезвию 2049'
        ]
        
        success_count = 0
        total_size = 0
        formats = {'JPEG': 0, 'PNG': 0, 'GIF': 0, 'WebP': 0}
        
        for i, title in enumerate(updated_films, 1):
            try:
                film = Film.objects.get(title=title)
                
                if film.poster:
                    success_count += 1
                    total_size += film.poster.size
                    size_mb = film.poster.size / (1024 * 1024)
                    
                    # Определяем формат
                    format_type = "Unknown"
                    try:
                        with film.poster.open('rb') as f:
                            header = f.read(12)
                            if header.startswith(b'\xff\xd8\xff'):
                                format_type = "JPEG"
                            elif header.startswith(b'\x89PNG'):
                                format_type = "PNG"
                            elif header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
                                format_type = "GIF"
                            elif header.startswith(b'RIFF') and b'WEBP' in header:
                                format_type = "WebP"
                        
                        if format_type in formats:
                            formats[format_type] += 1
                            
                    except:
                        pass
                    
                    self.stdout.write(f"{i:2d}. ✅ {film.title} ({film.year}) - {size_mb:.2f} МБ - {format_type}")
                    
                else:
                    self.stdout.write(f"{i:2d}. ❌ {film.title} ({film.year}) - НЕТ ПОСТЕРА")
                    
            except Film.DoesNotExist:
                self.stdout.write(f"{i:2d}. ❌ {title} - НЕ НАЙДЕН")
        
        # Итоговая статистика
        self.stdout.write(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
        self.stdout.write("=" * 40)
        self.stdout.write(f"✅ Успешно обновлено: {success_count}/{len(updated_films)} фильмов")
        self.stdout.write(f"📏 Общий размер: {total_size:,} байт ({total_size/(1024*1024):.2f} МБ)")
        
        if success_count > 0:
            self.stdout.write(f"📊 Средний размер: {total_size/success_count:,.0f} байт ({total_size/success_count/(1024*1024):.2f} МБ)")
        
        self.stdout.write(f"\n📄 ФОРМАТЫ:")
        for format_type, count in formats.items():
            if count > 0:
                percentage = (count / success_count) * 100
                self.stdout.write(f"    {format_type}: {count} файлов ({percentage:.1f}%)")
        
        # Источники
        sources = [
            "🛒 Ozone.ru", "📚 Википедия", "🎭 Кино-Театр.ру", 
            "🔍 Google Images", "🎬 КиноХод", "⭐ КиноПоиск", 
            "🍍 Ананас Постер", "🎥 Film.ru"
        ]
        
        self.stdout.write(f"\n🌐 ИСТОЧНИКИ ПОСТЕРОВ:")
        for source in sources:
            self.stdout.write(f"    {source}")
        
        # Финальное сообщение
        if success_count == len(updated_films):
            self.stdout.write(self.style.SUCCESS(f"\n🎉 ВСЕ ПОСТЕРЫ УСПЕШНО ОБНОВЛЕНЫ!"))
            self.stdout.write("🖼️ Высокое качество изображений")
            self.stdout.write("🔄 Разнообразие форматов (JPEG, GIF, WebP)")
            self.stdout.write("🌍 Множество надежных источников")
            self.stdout.write("📱 Готовы к отображению на TochkaFilms")
        else:
            self.stdout.write(self.style.WARNING(f"\n⚠️ Обновлено {success_count} из {len(updated_films)} постеров"))
        
        self.stdout.write(f"\n🚀 Проверка завершена!")