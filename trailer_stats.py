from django.core.management.base import BaseCommand
from films.models import Film
from urllib.parse import urlparse


class Command(BaseCommand):
    help = 'Показывает статистику по трейлерам'

    def handle(self, *args, **options):
        self.show_detailed_statistics()

    def show_detailed_statistics(self):
        """Показывает детальную статистику по трейлерам"""
        films = Film.objects.all()
        
        # Основная статистика
        stats = {
            'total': films.count(),
            'with_trailers': films.exclude(trailer_url='').count(),
            'without_trailers': films.filter(trailer_url='').count(),
        }
        
        # Статистика по источникам
        sources = {
            'kinopoisk': films.filter(trailer_url__icontains='kinopoisk.ru').count(),
            'rutube': films.filter(trailer_url__icontains='rutube.ru').count(),
            'vk': films.filter(trailer_url__icontains='vk.com').count(),
            'ok': films.filter(trailer_url__icontains='ok.ru').count(),
            'youtube': films.filter(trailer_url__icontains='youtube.com').count(),
            'mail': films.filter(trailer_url__icontains='mail.ru').count(),
            'ivi': films.filter(trailer_url__icontains='ivi.ru').count(),
            'other': 0
        }
        
        # Подсчитываем "другие"
        known_sources = sum(sources.values())
        sources['other'] = stats['with_trailers'] - known_sources
        
        # Вывод статистики
        self.stdout.write("=" * 50)
        self.stdout.write("📊 СТАТИСТИКА ТРЕЙЛЕРОВ")
        self.stdout.write("=" * 50)
        
        self.stdout.write(f"\n📈 ОБЩАЯ СТАТИСТИКА:")
        self.stdout.write(f"  Всего фильмов: {stats['total']}")
        self.stdout.write(f"  С трейлерами: {stats['with_trailers']} ({stats['with_trailers']/stats['total']*100:.1f}%)")
        self.stdout.write(f"  Без трейлеров: {stats['without_trailers']}")
        
        if stats['with_trailers'] > 0:
            self.stdout.write(f"\n🎬 ИСТОЧНИКИ ТРЕЙЛЕРОВ:")
            
            # Сортируем источники по количеству
            sorted_sources = sorted(sources.items(), key=lambda x: x[1], reverse=True)
            
            for source, count in sorted_sources:
                if count > 0:
                    percentage = count / stats['with_trailers'] * 100
                    icon = self.get_source_icon(source)
                    name = self.get_source_name(source)
                    self.stdout.write(f"  {icon} {name}: {count} ({percentage:.1f}%)")
        
        # Топ фильмы по источникам
        self.show_top_films_by_source()
        
        # Рекомендации
        self.show_recommendations(stats, sources)

    def get_source_icon(self, source):
        """Возвращает иконку для источника"""
        icons = {
            'kinopoisk': '🎭',
            'rutube': '📺',
            'vk': '👥',
            'ok': '🔗',
            'youtube': '🌐',
            'mail': '📧',
            'ivi': '📱',
            'other': '❓'
        }
        return icons.get(source, '❓')

    def get_source_name(self, source):
        """Возвращает название источника"""
        names = {
            'kinopoisk': 'Кинопоиск',
            'rutube': 'Rutube',
            'vk': 'VK Video',
            'ok': 'OK.ru',
            'youtube': 'YouTube',
            'mail': 'Mail.ru',
            'ivi': 'ivi.ru',
            'other': 'Другие'
        }
        return names.get(source, 'Неизвестный')

    def show_top_films_by_source(self):
        """Показывает примеры фильмов по источникам"""
        self.stdout.write(f"\n🏆 ПРИМЕРЫ ФИЛЬМОВ ПО ИСТОЧНИКАМ:")
        
        sources_to_check = ['kinopoisk', 'rutube', 'vk']
        
        for source in sources_to_check:
            if source == 'kinopoisk':
                films = Film.objects.filter(trailer_url__icontains='kinopoisk.ru')[:3]
            elif source == 'rutube':
                films = Film.objects.filter(trailer_url__icontains='rutube.ru')[:3]
            elif source == 'vk':
                films = Film.objects.filter(trailer_url__icontains='vk.com')[:3]
            
            if films:
                icon = self.get_source_icon(source)
                name = self.get_source_name(source)
                self.stdout.write(f"\n  {icon} {name}:")
                for film in films:
                    self.stdout.write(f"    • {film.title} ({film.year})")

    def show_recommendations(self, stats, sources):
        """Показывает рекомендации по улучшению"""
        self.stdout.write(f"\n💡 РЕКОМЕНДАЦИИ:")
        
        if stats['without_trailers'] > 0:
            self.stdout.write(f"  ⚠️  Добавить трейлеры для {stats['without_trailers']} фильмов")
            self.stdout.write(f"     Команда: python manage.py add_trailers --all-missing")
        
        if sources['youtube'] > 0:
            self.stdout.write(f"  🔄 Заменить {sources['youtube']} YouTube трейлеров на русскоязычные")
            self.stdout.write(f"     Команда: python manage.py update_russian_trailers --popular-only")
        
        if sources['kinopoisk'] < 20:
            self.stdout.write(f"  ⬆️  Увеличить количество трейлеров с Кинопоиска")
            self.stdout.write(f"     Команда: python manage.py update_russian_trailers --source kinopoisk")
        
        if stats['with_trailers'] == stats['total']:
            self.stdout.write(f"  ✅ Отлично! Все фильмы имеют трейлеры")
        
        self.stdout.write(f"\n📋 ПОЛЕЗНЫЕ КОМАНДЫ:")
        self.stdout.write(f"  • Проверка: python manage.py check_trailers")
        self.stdout.write(f"  • Обновление: python manage.py update_russian_trailers --popular-only")
        self.stdout.write(f"  • Поиск: python manage.py find_real_trailers --search 'название'")

    def show_quality_analysis(self):
        """Анализ качества трейлеров"""
        films = Film.objects.exclude(trailer_url='')
        
        quality_stats = {
            'hd': 0,
            'official': 0,
            'russian': 0,
            'embed': 0
        }
        
        for film in films:
            url = film.trailer_url.lower()
            
            if 'hd' in url or 'high' in url:
                quality_stats['hd'] += 1
            
            if 'official' in url or 'trailer' in url:
                quality_stats['official'] += 1
            
            if 'russian' in url or 'ru' in url or 'kinopoisk' in url:
                quality_stats['russian'] += 1
            
            if 'embed' in url or 'onlyPlayer' in url:
                quality_stats['embed'] += 1
        
        self.stdout.write(f"\n🎯 АНАЛИЗ КАЧЕСТВА:")
        self.stdout.write(f"  📺 HD качество: {quality_stats['hd']}")
        self.stdout.write(f"  🎬 Официальные: {quality_stats['official']}")
        self.stdout.write(f"  🇷🇺 Русскоязычные: {quality_stats['russian']}")
        self.stdout.write(f"  🔗 Встраиваемые: {quality_stats['embed']}")

    def export_trailer_list(self):
        """Экспортирует список всех трейлеров"""
        films = Film.objects.exclude(trailer_url='').order_by('title')
        
        self.stdout.write(f"\n📄 СПИСОК ВСЕХ ТРЕЙЛЕРОВ:")
        self.stdout.write("-" * 80)
        
        for film in films:
            domain = urlparse(film.trailer_url).netloc
            self.stdout.write(f"{film.title} ({film.year}) - {domain}")
            self.stdout.write(f"  {film.trailer_url}")
            self.stdout.write("")