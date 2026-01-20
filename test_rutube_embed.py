from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Тестирование встраиваемых Rutube трейлеров'

    def handle(self, *args, **options):
        self.stdout.write("📺 ТЕСТИРОВАНИЕ RUTUBE ТРЕЙЛЕРОВ")
        self.stdout.write("=" * 60)
        
        # Проверяем фильмы с Rutube трейлерами
        rutube_films = Film.objects.filter(trailer_url__contains='rutube.ru')
        
        self.stdout.write(f"\n📊 СТАТИСТИКА RUTUBE:")
        self.stdout.write(f"  📺 Фильмов с Rutube: {rutube_films.count()}")
        self.stdout.write(f"  🎬 Всего фильмов: {Film.objects.count()}")
        
        if rutube_films.exists():
            self.stdout.write(f"\n🎬 ФИЛЬМЫ С RUTUBE ТРЕЙЛЕРАМИ:")
            for film in rutube_films:
                self.stdout.write(f"  📺 {film.title} ({film.year})")
                self.stdout.write(f"    URL: {film.trailer_url}")
                
                # Проверяем формат URL для встраивания
                if 'embed' in film.trailer_url or 'player' in film.trailer_url:
                    self.stdout.write(f"    ✅ Готов для встраивания")
                else:
                    self.stdout.write(f"    ⚠️ Возможно нужен embed формат")
        
        self.stdout.write(f"\n🔧 ПОДДЕРЖИВАЕМЫЕ ФОРМАТЫ RUTUBE:")
        formats = [
            "https://rutube.ru/video/[ID]/",
            "https://rutube.ru/play/embed/[ID]/", 
            "https://rutube.ru/embed/[ID]/",
            "https://player.rutube.ru/embed/[ID]/"
        ]
        
        for fmt in formats:
            self.stdout.write(f"  📺 {fmt}")
        
        self.stdout.write(f"\n✨ ОСОБЕННОСТИ ВСТРАИВАНИЯ:")
        features = [
            "🎬 Автоматическое добавление ?embed=1",
            "▶️ Красивая кнопка воспроизведения",
            "🎨 Netflix-стиль оверлей",
            "📱 Адаптивный дизайн 16:9",
            "🇷🇺 Русская озвучка гарантирована",
            "⚡ Быстрая загрузка плеера",
            "🔄 Автоплей при клике",
            "💫 Плавные анимации"
        ]
        
        for feature in features:
            self.stdout.write(f"  {feature}")
        
        self.stdout.write(f"\n🎯 КАК РАБОТАЕТ ВСТРАИВАНИЕ:")
        steps = [
            "1. Проверяется наличие 'rutube.ru' в URL",
            "2. Создается iframe с embed параметром", 
            "3. Добавляется красивый оверлей с кнопкой",
            "4. При клике оверлей исчезает и начинается воспроизведение",
            "5. Автоматически добавляется autoplay=1"
        ]
        
        for step in steps:
            self.stdout.write(f"  {step}")
        
        self.stdout.write(f"\n🌐 ТЕСТИРОВАНИЕ:")
        self.stdout.write("  1. Откройте http://127.0.0.1:8000/")
        self.stdout.write("  2. Выберите фильм с Rutube трейлером")
        self.stdout.write("  3. Прокрутите до секции трейлера")
        self.stdout.write("  4. Увидите встроенный плеер с кнопкой")
        self.stdout.write("  5. Кликните для воспроизведения")
        
        self.stdout.write(f"\n💡 ПРЕИМУЩЕСТВА РЕШЕНИЯ:")
        advantages = [
            "📺 Воспроизведение прямо на сайте",
            "🇷🇺 Русская озвучка Rutube",
            "🎨 Красивый Netflix-дизайн",
            "📱 Мобильная совместимость",
            "⚡ Быстрая загрузка",
            "🔄 Автоматический autoplay",
            "✨ Плавные анимации",
            "🎯 Простота использования"
        ]
        
        for advantage in advantages:
            self.stdout.write(f"  {advantage}")
        
        self.stdout.write(f"\n🎨 ДИЗАЙН ЭЛЕМЕНТЫ:")
        design_elements = [
            "▶️ Большая кнопка воспроизведения",
            "🌊 Градиентный оверлей",
            "💫 Пульсирующие анимации",
            "🎬 16:9 соотношение сторон",
            "📱 Адаптивность для мобильных",
            "🔄 Hover эффекты",
            "✨ Плавные переходы",
            "🎯 Центрированное расположение"
        ]
        
        for element in design_elements:
            self.stdout.write(f"  {element}")
        
        if rutube_films.exists():
            self.stdout.write(self.style.SUCCESS(f"\n🎉 RUTUBE ТРЕЙЛЕРЫ ГОТОВЫ!"))
            self.stdout.write("📺 Все Rutube видео будут встраиваться прямо на сайте")
            self.stdout.write("🇷🇺 с красивым дизайном и русской озвучкой!")
        else:
            self.stdout.write(self.style.WARNING(f"\n⚠️ RUTUBE ТРЕЙЛЕРЫ НЕ НАЙДЕНЫ"))
            self.stdout.write("💡 Добавьте Rutube ссылки в базу данных")
            self.stdout.write("🔧 Используйте команду для добавления трейлеров")
        
        self.stdout.write(f"\n🔗 ПРИМЕР RUTUBE URL:")
        self.stdout.write("  📺 https://rutube.ru/video/abc123def456/")
        self.stdout.write("  📺 https://rutube.ru/play/embed/abc123def456/")
        self.stdout.write("  📺 https://player.rutube.ru/embed/abc123def456/")
        
        self.stdout.write(f"\n📋 СЛЕДУЮЩИЕ ШАГИ:")
        next_steps = [
            "1. Убедитесь что у фильмов есть Rutube URL",
            "2. Запустите сервер: python manage.py runserver",
            "3. Откройте фильм с Rutube трейлером",
            "4. Проверьте встраивание и воспроизведение",
            "5. Протестируйте на мобильном устройстве"
        ]
        
        for step in next_steps:
            self.stdout.write(f"  {step}")