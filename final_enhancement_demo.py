from django.core.management.base import BaseCommand
from films.models import Film, Category


class Command(BaseCommand):
    help = 'Финальная демонстрация всех улучшений TochkaFilms'

    def handle(self, *args, **options):
        self.stdout.write("🎬 ФИНАЛЬНАЯ ДЕМОНСТРАЦИЯ TOCHKAFILMS")
        self.stdout.write("=" * 60)
        
        # Общая статистика
        total_films = Film.objects.count()
        total_categories = Category.objects.count()
        
        # Статистика постеров
        films_with_posters = Film.objects.exclude(poster='').count()
        poster_coverage = (films_with_posters / total_films * 100) if total_films > 0 else 0
        
        # Статистика трейлеров
        films_with_trailers = Film.objects.exclude(trailer_url='').count()
        trailer_coverage = (films_with_trailers / total_films * 100) if total_films > 0 else 0
        
        # Статистика описаний
        films_with_long_descriptions = 0
        for film in Film.objects.all():
            if len(film.description) >= 300:
                films_with_long_descriptions += 1
        description_coverage = (films_with_long_descriptions / total_films * 100) if total_films > 0 else 0
        
        # Статистика по категориям
        category_stats = []
        for category in Category.objects.all():
            film_count = category.films.count()
            category_stats.append((category.name, film_count))
        category_stats.sort(key=lambda x: x[1], reverse=True)
        
        self.stdout.write("📊 ОБЩАЯ СТАТИСТИКА КОЛЛЕКЦИИ:")
        self.stdout.write(f"  🎬 Всего фильмов: {total_films}")
        self.stdout.write(f"  📂 Категорий: {total_categories}")
        self.stdout.write(f"  🖼️ Покрытие постерами: {poster_coverage:.1f}% ({films_with_posters}/{total_films})")
        self.stdout.write(f"  🎥 Покрытие трейлерами: {trailer_coverage:.1f}% ({films_with_trailers}/{total_films})")
        self.stdout.write(f"  📝 Подробные описания: {description_coverage:.1f}% ({films_with_long_descriptions}/{total_films})")
        
        self.stdout.write(f"\n📂 СТАТИСТИКА ПО КАТЕГОРИЯМ:")
        for category_name, count in category_stats[:10]:  # Топ 10 категорий
            self.stdout.write(f"  🎭 {category_name}: {count} фильмов")
        
        # Примеры улучшенных фильмов
        self.stdout.write(f"\n🌟 ПРИМЕРЫ УЛУЧШЕННЫХ ФИЛЬМОВ:")
        
        # Фильмы с трейлерами Rutube
        rutube_films = Film.objects.filter(trailer_url__contains='rutube.ru')[:5]
        if rutube_films:
            self.stdout.write(f"  📺 Фильмы с Rutube трейлерами:")
            for film in rutube_films:
                self.stdout.write(f"    🇷🇺 {film.title} ({film.year})")
        
        # Фильмы с оригинальными постерами
        original_poster_films = Film.objects.filter(poster__contains='original')[:5]
        if original_poster_films:
            self.stdout.write(f"  🖼️ Фильмы с оригинальными постерами:")
            for film in original_poster_films:
                self.stdout.write(f"    🎨 {film.title} ({film.year})")
        
        # Фильмы с подробными описаниями
        detailed_films = []
        for film in Film.objects.all():
            if len(film.description) >= 400:
                detailed_films.append(film)
        
        if detailed_films:
            self.stdout.write(f"  📝 Фильмы с подробными описаниями:")
            for film in detailed_films[:5]:
                desc_length = len(film.description)
                self.stdout.write(f"    📚 {film.title} ({desc_length} символов)")
        
        # Франшизы
        self.stdout.write(f"\n🎬 ФРАНШИЗЫ И СЕРИИ:")
        scream_films = Film.objects.filter(title__startswith='Крик').count()
        if scream_films > 0:
            self.stdout.write(f"  🔪 Крик: {scream_films} фильмов")
        
        terminator_films = Film.objects.filter(title__startswith='Терминатор').count()
        if terminator_films > 0:
            self.stdout.write(f"  🤖 Терминатор: {terminator_films} фильмов")
        
        # Технические улучшения
        self.stdout.write(f"\n⚡ ТЕХНИЧЕСКИЕ УЛУЧШЕНИЯ:")
        self.stdout.write(f"  🎨 Netflix-стиль дизайн с красной темой")
        self.stdout.write(f"  🔤 Красивые шрифты: Orbitron, Inter, Playfair Display")
        self.stdout.write(f"  📱 Полная адаптивность для мобильных устройств")
        self.stdout.write(f"  🎭 Анимации и эффекты наведения")
        self.stdout.write(f"  🇷🇺 Русские платформы для трейлеров")
        self.stdout.write(f"  🔍 Улучшенный поиск по всем параметрам")
        self.stdout.write(f"  📊 Система рекомендаций и топ фильмов")
        self.stdout.write(f"  🔔 Уведомления и история просмотров")
        
        # Функциональные возможности
        self.stdout.write(f"\n🚀 ФУНКЦИОНАЛЬНЫЕ ВОЗМОЖНОСТИ:")
        self.stdout.write(f"  👤 Система пользователей и профилей")
        self.stdout.write(f"  ❤️ Избранное и список к просмотру")
        self.stdout.write(f"  ⭐ Система оценок и отзывов")
        self.stdout.write(f"  🎯 Фильтрация по категориям, году, рейтингу")
        self.stdout.write(f"  📈 Топ фильмов по различным критериям")
        self.stdout.write(f"  🔄 Рекомендации на основе просмотров")
        self.stdout.write(f"  📱 Адаптивный интерфейс")
        
        # Качество контента
        self.stdout.write(f"\n✨ КАЧЕСТВО КОНТЕНТА:")
        self.stdout.write(f"  🖼️ Оригинальные постеры высокого качества")
        self.stdout.write(f"  🎥 Трейлеры с русской озвучкой")
        self.stdout.write(f"  📝 Подробные описания с деталями сюжета")
        self.stdout.write(f"  🎭 Информация об актерах и режиссерах")
        self.stdout.write(f"  🏆 Награды и достижения фильмов")
        
        # Статистика по годам
        year_stats = {}
        for film in Film.objects.all():
            decade = (film.year // 10) * 10
            year_stats[decade] = year_stats.get(decade, 0) + 1
        
        if year_stats:
            self.stdout.write(f"\n📅 РАСПРЕДЕЛЕНИЕ ПО ДЕСЯТИЛЕТИЯМ:")
            for decade in sorted(year_stats.keys(), reverse=True):
                count = year_stats[decade]
                self.stdout.write(f"  📆 {decade}е: {count} фильмов")
        
        # Заключение
        self.stdout.write(f"\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("🎉 TOCHKAFILMS - ГОТОВ К ИСПОЛЬЗОВАНИЮ!"))
        self.stdout.write("🌟 Полнофункциональный Netflix-стиль кинопортал")
        self.stdout.write("🇷🇺 С русскими трейлерами и локализацией")
        self.stdout.write("📱 Адаптивный дизайн для всех устройств")
        self.stdout.write("🎬 Богатая коллекция из 109+ фильмов")
        self.stdout.write("✨ Современный интерфейс и функциональность")
        
        self.stdout.write(f"\n🚀 ЗАПУСК СЕРВЕРА:")
        self.stdout.write("   python manage.py runserver")
        self.stdout.write("   Откройте: http://127.0.0.1:8000")
        
        self.stdout.write(f"\n👤 АДМИН-ПАНЕЛЬ:")
        self.stdout.write("   http://127.0.0.1:8000/admin/")
        self.stdout.write("   Создайте суперпользователя: python manage.py createsuperuser")
        
        self.stdout.write(self.style.SUCCESS(f"\n🎬 Добро пожаловать в TochkaFilms!"))