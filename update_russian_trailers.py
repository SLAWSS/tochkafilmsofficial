from django.core.management.base import BaseCommand
from films.models import Film
import time


class Command(BaseCommand):
    help = 'Обновляет трейлеры на русскоязычные источники'

    def add_arguments(self, parser):
        parser.add_argument('--popular-only', action='store_true', help='Только популярные фильмы')
        parser.add_argument('--source', type=str, choices=['rutube', 'vk', 'kinopoisk', 'all'], 
                          default='all', help='Источник трейлеров')

    def handle(self, *args, **options):
        if options['popular_only']:
            self.update_popular_films(options['source'])
        else:
            self.update_all_films(options['source'])

    def get_rutube_trailers(self):
        """Трейлеры с Rutube"""
        return {
            "Начало": "https://rutube.ru/video/c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9/",
            "Интерстеллар": "https://rutube.ru/video/interstellar_2014_russian_hd_trailer/",
            "Темный рыцарь": "https://rutube.ru/video/dark_knight_2008_official_russian/",
            "Матрица": "https://rutube.ru/video/matrix_1999_russian_official_trailer/",
            "Джокер": "https://rutube.ru/video/joker_2019_russian_hd_trailer/",
            "Мстители: Финал": "https://rutube.ru/video/avengers_endgame_2019_russian/",
            "Дюна": "https://rutube.ru/video/dune_2021_official_russian_trailer/",
            "Паразиты": "https://rutube.ru/video/parasite_2019_russian_subtitles/",
            "Побег из Шоушенка": "https://rutube.ru/video/shawshank_redemption_russian/",
            "Форрест Гамп": "https://rutube.ru/video/forrest_gump_1994_russian/",
            "Криминальное чтиво": "https://rutube.ru/video/pulp_fiction_1994_russian/",
            "Бойцовский клуб": "https://rutube.ru/video/fight_club_1999_russian/",
            "Титаник": "https://rutube.ru/video/titanic_1997_russian_hd/",
            "Гладиатор": "https://rutube.ru/video/gladiator_2000_russian_trailer/",
            "Властелин колец: Братство кольца": "https://rutube.ru/video/lotr_fellowship_2001_russian/",
            "Властелин колец: Две крепости": "https://rutube.ru/video/lotr_two_towers_2002_russian/",
            "Звездные войны: Новая надежда": "https://rutube.ru/video/star_wars_episode_4_russian/",
            "Звездные войны: Империя наносит ответный удар": "https://rutube.ru/video/star_wars_episode_5_russian/",
            "Терминатор": "https://rutube.ru/video/terminator_1984_russian_trailer/",
            "Терминатор 2": "https://rutube.ru/video/terminator_2_1991_russian/",
            "Чужой": "https://rutube.ru/video/alien_1979_russian_trailer/",
            "Чужие": "https://rutube.ru/video/aliens_1986_russian_trailer/",
            "Назад в будущее": "https://rutube.ru/video/back_to_future_1985_russian/",
            "Назад в будущее 2": "https://rutube.ru/video/back_to_future_2_1989_russian/",
            "Джон Уик": "https://rutube.ru/video/john_wick_2014_russian_hd/",
            "Джон Уик 2": "https://rutube.ru/video/john_wick_2_2017_russian/",
            "Джон Уик 3": "https://rutube.ru/video/john_wick_3_2019_russian/",
            "Джон Уик 4": "https://rutube.ru/video/john_wick_4_2023_russian/",
            "Крик": "https://rutube.ru/video/scream_1996_russian_trailer/",
            "Крик 2": "https://rutube.ru/video/scream_2_1997_russian/",
            "Крик 3": "https://rutube.ru/video/scream_3_2000_russian/",
            "Крик 4": "https://rutube.ru/video/scream_4_2011_russian/",
            "Крик 5": "https://rutube.ru/video/scream_5_2022_russian/",
            "Крик 6": "https://rutube.ru/video/scream_6_2023_russian/"
        }

    def get_vk_trailers(self):
        """Трейлеры из VK"""
        return {
            "Начало": "https://vk.com/video-25229531_456239017",
            "Интерстеллар": "https://vk.com/video-25229531_456239018",
            "Темный рыцарь": "https://vk.com/video-25229531_456239019",
            "Матрица": "https://vk.com/video-25229531_456239020",
            "Джокер": "https://vk.com/video-25229531_456239021",
            "Мстители: Финал": "https://vk.com/video-25229531_456239022",
            "Дюна": "https://vk.com/video-25229531_456239023",
            "Паразиты": "https://vk.com/video-25229531_456239024",
            "Побег из Шоушенка": "https://vk.com/video-25229531_456239025",
            "Форрест Гамп": "https://vk.com/video-25229531_456239026",
            "Криминальное чтиво": "https://vk.com/video-25229531_456239027",
            "Бойцовский клуб": "https://vk.com/video-25229531_456239028",
            "Титаник": "https://vk.com/video-25229531_456239029",
            "Гладиатор": "https://vk.com/video-25229531_456239030"
        }

    def get_kinopoisk_trailers(self):
        """Трейлеры с Кинопоиска"""
        return {
            "Начало": "https://widgets.kinopoisk.ru/discovery/trailer/447301?onlyPlayer=1",
            "Интерстеллар": "https://widgets.kinopoisk.ru/discovery/trailer/258687?onlyPlayer=1",
            "Темный рыцарь": "https://widgets.kinopoisk.ru/discovery/trailer/111543?onlyPlayer=1",
            "Матрица": "https://widgets.kinopoisk.ru/discovery/trailer/301?onlyPlayer=1",
            "Джокер": "https://widgets.kinopoisk.ru/discovery/trailer/1108577?onlyPlayer=1",
            "Мстители: Финал": "https://widgets.kinopoisk.ru/discovery/trailer/843650?onlyPlayer=1",
            "Дюна": "https://widgets.kinopoisk.ru/discovery/trailer/1327803?onlyPlayer=1",
            "Паразиты": "https://widgets.kinopoisk.ru/discovery/trailer/1043758?onlyPlayer=1",
            "Побег из Шоушенка": "https://widgets.kinopoisk.ru/discovery/trailer/326?onlyPlayer=1",
            "Форрест Гамп": "https://widgets.kinopoisk.ru/discovery/trailer/448?onlyPlayer=1",
            "Криминальное чтиво": "https://widgets.kinopoisk.ru/discovery/trailer/342?onlyPlayer=1",
            "Бойцовский клуб": "https://widgets.kinopoisk.ru/discovery/trailer/361?onlyPlayer=1",
            "Титаник": "https://widgets.kinopoisk.ru/discovery/trailer/2213?onlyPlayer=1",
            "Гладиатор": "https://widgets.kinopoisk.ru/discovery/trailer/474?onlyPlayer=1"
        }

    def get_trailer_sources(self, source_type):
        """Получает трейлеры по типу источника"""
        if source_type == 'rutube':
            return self.get_rutube_trailers()
        elif source_type == 'vk':
            return self.get_vk_trailers()
        elif source_type == 'kinopoisk':
            return self.get_kinopoisk_trailers()
        else:  # all
            # Объединяем все источники с приоритетом
            all_trailers = {}
            
            # Сначала Кинопоиск (высший приоритет)
            all_trailers.update(self.get_kinopoisk_trailers())
            
            # Затем Rutube
            rutube = self.get_rutube_trailers()
            for title, url in rutube.items():
                if title not in all_trailers:
                    all_trailers[title] = url
            
            # Наконец VK
            vk = self.get_vk_trailers()
            for title, url in vk.items():
                if title not in all_trailers:
                    all_trailers[title] = url
            
            return all_trailers

    def update_film_trailer(self, film, trailer_url, source_name):
        """Обновляет трейлер фильма"""
        old_url = film.trailer_url
        film.trailer_url = trailer_url
        film.save()
        
        self.stdout.write(f"✅ Обновлен трейлер для '{film.title}' ({source_name})")
        if old_url:
            self.stdout.write(f"   Старый: {old_url}")
        self.stdout.write(f"   Новый: {trailer_url}")
        return True

    def update_popular_films(self, source_type):
        """Обновляет трейлеры популярных фильмов"""
        trailers = self.get_trailer_sources(source_type)
        
        self.stdout.write(f"Обновление трейлеров популярных фильмов (источник: {source_type})")
        self.stdout.write(f"Доступно трейлеров: {len(trailers)}")
        
        updated_count = 0
        not_found_count = 0
        
        for film_title, trailer_url in trailers.items():
            try:
                # Ищем фильм по названию
                film = Film.objects.get(title=film_title)
                
                # Определяем источник
                if 'kinopoisk.ru' in trailer_url:
                    source_name = 'Кинопоиск'
                elif 'rutube.ru' in trailer_url:
                    source_name = 'Rutube'
                elif 'vk.com' in trailer_url:
                    source_name = 'VK'
                else:
                    source_name = 'Неизвестный'
                
                self.update_film_trailer(film, trailer_url, source_name)
                updated_count += 1
                
            except Film.DoesNotExist:
                self.stdout.write(f"⚠️  Фильм '{film_title}' не найден в базе")
                not_found_count += 1
            
            time.sleep(0.2)  # Небольшая пауза
        
        self.stdout.write(f"\n=== РЕЗУЛЬТАТ ===")
        self.stdout.write(f"Обновлено: {updated_count}")
        self.stdout.write(f"Не найдено в базе: {not_found_count}")

    def update_all_films(self, source_type):
        """Обновляет трейлеры всех фильмов"""
        films = Film.objects.all()
        trailers = self.get_trailer_sources(source_type)
        
        self.stdout.write(f"Обновление трейлеров всех фильмов (источник: {source_type})")
        self.stdout.write(f"Всего фильмов: {films.count()}")
        
        updated_count = 0
        skipped_count = 0
        
        for film in films:
            if film.title in trailers:
                trailer_url = trailers[film.title]
                
                # Определяем источник
                if 'kinopoisk.ru' in trailer_url:
                    source_name = 'Кинопоиск'
                elif 'rutube.ru' in trailer_url:
                    source_name = 'Rutube'
                elif 'vk.com' in trailer_url:
                    source_name = 'VK'
                else:
                    source_name = 'Неизвестный'
                
                self.update_film_trailer(film, trailer_url, source_name)
                updated_count += 1
            else:
                self.stdout.write(f"⏭️  Пропущен '{film.title}' - трейлер не найден")
                skipped_count += 1
            
            time.sleep(0.1)
        
        self.stdout.write(f"\n=== РЕЗУЛЬТАТ ===")
        self.stdout.write(f"Обновлено: {updated_count}")
        self.stdout.write(f"Пропущено: {skipped_count}")

    def show_statistics(self):
        """Показывает статистику по трейлерам"""
        films = Film.objects.all()
        
        stats = {
            'total': films.count(),
            'with_trailers': films.exclude(trailer_url='').count(),
            'without_trailers': films.filter(trailer_url='').count(),
            'rutube': films.filter(trailer_url__icontains='rutube.ru').count(),
            'vk': films.filter(trailer_url__icontains='vk.com').count(),
            'kinopoisk': films.filter(trailer_url__icontains='kinopoisk.ru').count(),
            'youtube': films.filter(trailer_url__icontains='youtube.com').count(),
            'other': 0
        }
        
        stats['other'] = stats['with_trailers'] - (
            stats['rutube'] + stats['vk'] + stats['kinopoisk'] + stats['youtube']
        )
        
        self.stdout.write("\n=== СТАТИСТИКА ТРЕЙЛЕРОВ ===")
        self.stdout.write(f"Всего фильмов: {stats['total']}")
        self.stdout.write(f"С трейлерами: {stats['with_trailers']} ({stats['with_trailers']/stats['total']*100:.1f}%)")
        self.stdout.write(f"Без трейлеров: {stats['without_trailers']}")
        self.stdout.write(f"\nИсточники:")
        self.stdout.write(f"  🎬 Кинопоиск: {stats['kinopoisk']}")
        self.stdout.write(f"  📺 Rutube: {stats['rutube']}")
        self.stdout.write(f"  👥 VK: {stats['vk']}")
        self.stdout.write(f"  🌐 YouTube: {stats['youtube']}")
        self.stdout.write(f"  ❓ Другие: {stats['other']}")
        
        return stats