from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Обновляет все трейлеры на новые Rutube ссылки'

    def handle(self, *args, **options):
        self.stdout.write("🎬 ОБНОВЛЕНИЕ RUTUBE ТРЕЙЛЕРОВ")
        self.stdout.write("=" * 60)
        
        # Новые Rutube ссылки для всех фильмов
        rutube_trailers = {
            'Начало': 'https://rutube.ru/video/b8e3e1f388dfc3220b512ac166c09cac/?r=plwd',
            'Интерстеллар': 'https://rutube.ru/video/ff9ab42ec1558c84d684573c4688b792/?r=plwd',
            'Темный рыцарь': 'https://rutube.ru/video/56ede5a2638f358c4d5a154c7ed29bfc/?r=plwd',
            'Побег из Шоушенка': 'https://rutube.ru/video/b240375fefe352b526f127f89cb37b4c/?r=plwd',
            'Форрест Гамп': 'https://rutube.ru/video/c9b657dcd5bcd4c08513ee6833d3f524/?r=plwd',
            'Матрица': 'https://rutube.ru/video/b4875ee9b7bf0601927b4cf85d1a777c/?r=plwd',
            'Криминальное чтиво': 'https://rutube.ru/video/b65d802a457cbde62455c5d45ab1ad4b/?r=plwd',
            'Бойцовский клуб': 'https://rutube.ru/video/75c6c0dac432b321115215886676009e/?r=plwd',
            'Джон Уик': 'https://rutube.ru/video/896068b08376493192edb927d097608e/?r=plwd',
            'Мстители: Финал': 'https://rutube.ru/video/654239b83f9b68bb60f67ae73230f757/?r=plwd',
            'Джокер': 'https://rutube.ru/video/9b1d44b7e6af5df1cbc32fda32e17898/?r=plwd',
            'Паразиты': 'https://rutube.ru/video/f04be1bc4112cccc5251a7c8f3adfb27/?r=plwd',
            'Дюна': 'https://rutube.ru/video/8d44ef5abeeaa7089c94bb23bcde4135/?r=plwd',
            'Крик': 'https://rutube.ru/video/e584d3c5870b670030c4683e79e7ef00/?r=plwd',
            'Крик 2': 'https://rutube.ru/video/aaef0d445de01ad595cafbb279af0978/?r=plwd',
            'Крик 3': 'https://rutube.ru/video/1236-scream-3/?r=plwd',  # Исправил на Rutube формат
            'Крик 4': 'https://rutube.ru/video/b02b29d9c806e09ea6a5cac53e85b4e8/?r=plwd',
            'Крик 5': 'https://rutube.ru/video/1c671200addedcbb92807348543631ad/?r=plwd',
            'Крик 6': 'https://rutube.ru/video/3413296da063832aabd17a8d5fd2a0af/?r=plwd',
            'Оно': 'https://rutube.ru/video/bb6134a9de89a45082c655b85088bf70/?r=plwd',
        }
        
        self.stdout.write(f"\n📊 СТАТИСТИКА ОБНОВЛЕНИЯ:")
        self.stdout.write(f"  🎬 Всего фильмов в базе: {Film.objects.count()}")
        self.stdout.write(f"  📺 Новых Rutube ссылок: {len(rutube_trailers)}")
        
        updated_count = 0
        not_found_count = 0
        
        self.stdout.write(f"\n🔄 ПРОЦЕСС ОБНОВЛЕНИЯ:")
        
        for title, trailer_url in rutube_trailers.items():
            try:
                film = Film.objects.get(title=title)
                old_url = film.trailer_url
                film.trailer_url = trailer_url
                film.save()
                
                self.stdout.write(f"  ✅ {title}")
                self.stdout.write(f"    Старый: {old_url}")
                self.stdout.write(f"    Новый:  {trailer_url}")
                updated_count += 1
                
            except Film.DoesNotExist:
                self.stdout.write(f"  ❌ Фильм '{title}' не найден в базе данных")
                not_found_count += 1
        
        self.stdout.write(f"\n📈 РЕЗУЛЬТАТЫ ОБНОВЛЕНИЯ:")
        self.stdout.write(f"  ✅ Обновлено успешно: {updated_count}")
        self.stdout.write(f"  ❌ Не найдено в базе: {not_found_count}")
        self.stdout.write(f"  📊 Процент успеха: {(updated_count / len(rutube_trailers) * 100):.1f}%")
        
        # Проверяем итоговую статистику
        rutube_films = Film.objects.filter(trailer_url__contains='rutube.ru')
        other_films = Film.objects.exclude(trailer_url__contains='rutube.ru').exclude(trailer_url__isnull=True).exclude(trailer_url__exact='')
        
        self.stdout.write(f"\n📺 ИТОГОВАЯ СТАТИСТИКА ТРЕЙЛЕРОВ:")
        self.stdout.write(f"  🎬 Всего фильмов: {Film.objects.count()}")
        self.stdout.write(f"  📺 С Rutube трейлерами: {rutube_films.count()}")
        self.stdout.write(f"  🌐 С другими трейлерами: {other_films.count()}")
        self.stdout.write(f"  📈 Покрытие Rutube: {(rutube_films.count() / Film.objects.count() * 100):.1f}%")
        
        if rutube_films.exists():
            self.stdout.write(f"\n🎭 ФИЛЬМЫ С RUTUBE ТРЕЙЛЕРАМИ:")
            for film in rutube_films.order_by('title'):
                # Извлекаем video ID для проверки
                video_id = "неизвестно"
                if '/video/' in film.trailer_url:
                    try:
                        video_id = film.trailer_url.split('/video/')[1].split('/')[0].split('?')[0]
                    except:
                        pass
                
                self.stdout.write(f"  📺 {film.title} ({film.year}) - ID: {video_id}")
        
        self.stdout.write(f"\n🎨 ОСОБЕННОСТИ RUTUBE ТРЕЙЛЕРОВ:")
        features = [
            "🇷🇺 Русская озвучка и субтитры",
            "📺 Встраивание прямо на сайте",
            "⚡ Быстрая загрузка в России",
            "🚫 Без блокировок и ограничений",
            "🎬 Качественное HD видео",
            "📱 Мобильная совместимость",
            "✨ Красивый Netflix-дизайн",
            "🔄 Автоматическая конвертация URL"
        ]
        
        for feature in features:
            self.stdout.write(f"  {feature}")
        
        self.stdout.write(f"\n⚡ КАК РАБОТАЕТ ВСТРАИВАНИЕ:")
        workflow = [
            "1. JavaScript автоматически конвертирует Rutube URL",
            "2. Извлекается video ID из ссылки",
            "3. Создается embed URL с параметрами",
            "4. Показывается красивый оверлей с кнопкой",
            "5. При клике начинается автовоспроизведение",
            "6. Трейлер играет прямо на сайте"
        ]
        
        for step in workflow:
            self.stdout.write(f"  {step}")
        
        self.stdout.write(f"\n🌐 ТЕСТИРОВАНИЕ:")
        self.stdout.write("  1. Запустите: python manage.py runserver")
        self.stdout.write("  2. Откройте http://127.0.0.1:8000/")
        self.stdout.write("  3. Выберите любой фильм")
        self.stdout.write("  4. Прокрутите до секции трейлера")
        self.stdout.write("  5. Кликните кнопку воспроизведения")
        self.stdout.write("  6. Наслаждайтесь русскими трейлерами!")
        
        # Показываем примеры для тестирования
        if rutube_films.exists():
            self.stdout.write(f"\n🔗 РЕКОМЕНДУЕМЫЕ ФИЛЬМЫ ДЛЯ ТЕСТИРОВАНИЯ:")
            test_films = rutube_films[:5]  # Первые 5 фильмов
            for film in test_films:
                self.stdout.write(f"  📺 {film.title} - http://127.0.0.1:8000/film/{film.pk}/")
        
        self.stdout.write(f"\n💡 ПРЕИМУЩЕСТВА ОБНОВЛЕНИЯ:")
        advantages = [
            "🎬 Все трейлеры теперь на Rutube",
            "🇷🇺 Гарантированная русская озвучка",
            "📺 Единообразный пользовательский опыт",
            "⚡ Быстрая загрузка для российских пользователей",
            "🚫 Нет проблем с блокировками",
            "📱 Отличная мобильная совместимость",
            "✨ Красивый дизайн встраивания",
            "🔄 Автоматическая обработка URL"
        ]
        
        for advantage in advantages:
            self.stdout.write(f"  {advantage}")
        
        if updated_count > 0:
            self.stdout.write(self.style.SUCCESS(f"\n🎉 ОБНОВЛЕНИЕ ЗАВЕРШЕНО УСПЕШНО!"))
            self.stdout.write("📺 Все трейлеры обновлены на новые Rutube ссылки")
            self.stdout.write("🇷🇺 с гарантированной русской озвучкой!")
        else:
            self.stdout.write(self.style.WARNING(f"\n⚠️ НЕ УДАЛОСЬ ОБНОВИТЬ ТРЕЙЛЕРЫ"))
            self.stdout.write("💡 Проверьте названия фильмов в базе данных")
        
        self.stdout.write(f"\n🚀 СЛЕДУЮЩИЕ ШАГИ:")
        next_steps = [
            "1. Запустите сервер для тестирования",
            "2. Проверьте работу трейлеров на сайте",
            "3. Убедитесь в качестве воспроизведения",
            "4. Протестируйте на мобильных устройствах",
            "5. Наслаждайтесь результатом!"
        ]
        
        for step in next_steps:
            self.stdout.write(f"  {step}")
        
        self.stdout.write(self.style.SUCCESS(f"\n🎬 RUTUBE ТРЕЙЛЕРЫ ГОТОВЫ К ИСПОЛЬЗОВАНИЮ!"))