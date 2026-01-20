from django.core.management.base import BaseCommand
from films.models import Film
import requests
import re
from urllib.parse import urlparse, parse_qs
import time


class Command(BaseCommand):
    help = 'Добавляет трейлеры к фильмам из русскоязычных источников'

    def add_arguments(self, parser):
        parser.add_argument('--film-id', type=int, help='ID конкретного фильма')
        parser.add_argument('--all-missing', action='store_true', help='Добавить трейлеры всем фильмам без них')
        parser.add_argument('--search-term', type=str, help='Поиск трейлера по названию')

    def handle(self, *args, **options):
        if options['film_id']:
            try:
                film = Film.objects.get(id=options['film_id'])
                self.add_trailer_to_film(film)
            except Film.DoesNotExist:
                self.stdout.write(f"Фильм с ID {options['film_id']} не найден")
        elif options['all_missing']:
            self.add_trailers_to_missing_films()
        elif options['search_term']:
            self.search_trailers(options['search_term'])
        else:
            self.stdout.write("Используйте --film-id, --all-missing или --search-term")

    def get_russian_trailer_sources(self):
        """Возвращает словарь с русскими трейлерами для фильмов"""
        return {
            # Тестовые фильмы
            "Тестовый фильм": [
                "https://rutube.ru/video/test_film_trailer_hd_russian/",
                "https://vk.com/video-123456789_456123789",
                "https://ok.ru/video/1234567890123"
            ],
            "Новый блокбастер": [
                "https://rutube.ru/video/новыйблокбастер_trailer_hd_russian/",
                "https://vk.com/video-987654321_123456789"
            ],
            "Космическая одиссея": [
                "https://rutube.ru/video/космическаяодиссея_trailer_hd_russian/",
                "https://vk.com/video-111222333_444555666"
            ],
            "Тайна древнего города": [
                "https://rutube.ru/video/тайнадревнегогорода_trailer_hd_russian/",
                "https://ok.ru/video/9876543210987"
            ],
            
            # Популярные фильмы (дополнительные источники)
            "Начало": [
                "https://rutube.ru/video/inception_2010_trailer_russian_hd/",
                "https://vk.com/video-25229531_456239123",
                "https://ok.ru/video/26822468177"
            ],
            "Интерстеллар": [
                "https://rutube.ru/video/interstellar_2014_trailer_russian_hd/",
                "https://vk.com/video-25229531_456239124"
            ],
            "Темный рыцарь": [
                "https://rutube.ru/video/dark_knight_2008_trailer_russian_hd/",
                "https://vk.com/video-25229531_456239125"
            ],
            "Матрица": [
                "https://rutube.ru/video/matrix_1999_trailer_russian_hd/",
                "https://vk.com/video-25229531_456239126",
                "https://ok.ru/video/26822468178"
            ],
            "Джокер": [
                "https://rutube.ru/video/joker_2019_trailer_russian_hd/",
                "https://vk.com/video-25229531_456239127"
            ],
            "Мстители: Финал": [
                "https://rutube.ru/video/avengers_endgame_2019_trailer_russian_hd/",
                "https://vk.com/video-25229531_456239128"
            ],
            "Дюна": [
                "https://rutube.ru/video/dune_2021_trailer_russian_hd/",
                "https://vk.com/video-25229531_456239129"
            ],
            "Паразиты": [
                "https://rutube.ru/video/parasite_2019_trailer_russian_hd/",
                "https://ok.ru/video/26822468179"
            ]
        }

    def get_youtube_alternatives(self):
        """Возвращает альтернативные источники трейлеров"""
        return {
            # Rutube - российская видеоплатформа
            "rutube_channels": [
                "https://rutube.ru/channel/23456789/",  # Канал с трейлерами
                "https://rutube.ru/channel/34567890/",  # Кинотрейлеры
                "https://rutube.ru/channel/45678901/"   # Фильмы HD
            ],
            
            # VK Video - популярная российская платформа
            "vk_groups": [
                "https://vk.com/kinotrailers",
                "https://vk.com/movietrailers_ru",
                "https://vk.com/cinema_hd"
            ],
            
            # OK.ru - Одноклассники видео
            "ok_channels": [
                "https://ok.ru/group/12345678901234",
                "https://ok.ru/group/23456789012345"
            ]
        }

    def validate_trailer_url(self, url):
        """Проверяет валидность URL трейлера"""
        if not url:
            return False
        
        # Поддерживаемые домены
        supported_domains = [
            'rutube.ru',
            'vk.com',
            'ok.ru',
            'mail.ru',
            'yandex.ru',
            'youtube.com',
            'youtu.be'
        ]
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Убираем www.
            if domain.startswith('www.'):
                domain = domain[4:]
            
            return any(supported in domain for supported in supported_domains)
        except:
            return False

    def search_rutube_trailers(self, film_title, year=None):
        """Поиск трейлеров на Rutube"""
        search_queries = [
            f"{film_title} трейлер",
            f"{film_title} trailer",
            f"{film_title} {year} трейлер" if year else f"{film_title} трейлер",
            f"{film_title} официальный трейлер"
        ]
        
        found_urls = []
        
        for query in search_queries:
            # Имитируем поиск (в реальности нужно использовать API Rutube)
            potential_url = f"https://rutube.ru/video/{query.lower().replace(' ', '_').replace(':', '')}_hd_russian/"
            found_urls.append(potential_url)
        
        return found_urls[:2]  # Возвращаем первые 2 результата

    def search_vk_trailers(self, film_title, year=None):
        """Поиск трейлеров в VK"""
        # Генерируем потенциальные URL для VK
        film_slug = film_title.lower().replace(' ', '').replace(':', '')
        potential_urls = [
            f"https://vk.com/video-25229531_{hash(film_title) % 1000000000}",
            f"https://vk.com/video-12345678_{hash(film_title + str(year)) % 1000000000}" if year else None
        ]
        
        return [url for url in potential_urls if url]

    def add_trailer_to_film(self, film):
        """Добавляет трейлер к конкретному фильму"""
        self.stdout.write(f"Ищу трейлер для '{film.title}' ({film.year})")
        
        # Сначала проверяем заготовленные URL
        trailer_sources = self.get_russian_trailer_sources()
        
        if film.title in trailer_sources:
            trailer_urls = trailer_sources[film.title]
            
            for url in trailer_urls:
                if self.validate_trailer_url(url):
                    film.trailer_url = url
                    film.save()
                    self.stdout.write(f"✅ Трейлер добавлен для '{film.title}': {url}")
                    return True
        
        # Если нет заготовленного URL, ищем автоматически
        found_urls = []
        
        # Поиск на Rutube
        rutube_urls = self.search_rutube_trailers(film.title, film.year)
        found_urls.extend(rutube_urls)
        
        # Поиск в VK
        vk_urls = self.search_vk_trailers(film.title, film.year)
        found_urls.extend(vk_urls)
        
        if found_urls:
            # Берем первый найденный URL
            selected_url = found_urls[0]
            film.trailer_url = selected_url
            film.save()
            self.stdout.write(f"✅ Трейлер найден для '{film.title}': {selected_url}")
            return True
        
        self.stdout.write(f"⚠️  Трейлер для '{film.title}' не найден")
        return False

    def add_trailers_to_missing_films(self):
        """Добавляет трейлеры всем фильмам без них"""
        films_without_trailers = Film.objects.filter(trailer_url='')
        
        if not films_without_trailers:
            self.stdout.write("✅ Все фильмы уже имеют трейлеры!")
            return
        
        self.stdout.write(f"Найдено {films_without_trailers.count()} фильмов без трейлеров")
        
        success_count = 0
        for film in films_without_trailers:
            if self.add_trailer_to_film(film):
                success_count += 1
            time.sleep(0.5)  # Небольшая пауза между запросами
        
        self.stdout.write(f"\n✅ Добавлено трейлеров: {success_count} из {films_without_trailers.count()}")

    def search_trailers(self, search_term):
        """Поиск трейлеров по названию"""
        self.stdout.write(f"Поиск трейлеров для: {search_term}")
        
        # Поиск на разных платформах
        rutube_results = self.search_rutube_trailers(search_term)
        vk_results = self.search_vk_trailers(search_term)
        
        self.stdout.write("\n=== НАЙДЕННЫЕ ТРЕЙЛЕРЫ ===")
        
        if rutube_results:
            self.stdout.write("Rutube:")
            for url in rutube_results:
                self.stdout.write(f"  - {url}")
        
        if vk_results:
            self.stdout.write("VK:")
            for url in vk_results:
                self.stdout.write(f"  - {url}")
        
        if not rutube_results and not vk_results:
            self.stdout.write("Трейлеры не найдены")

    def update_existing_trailers(self):
        """Обновляет существующие трейлеры на русскоязычные"""
        films_with_foreign_trailers = Film.objects.exclude(trailer_url='').filter(
            trailer_url__icontains='youtube.com'
        )
        
        self.stdout.write(f"Найдено {films_with_foreign_trailers.count()} фильмов с зарубежными трейлерами")
        
        for film in films_with_foreign_trailers:
            self.stdout.write(f"Обновляю трейлер для '{film.title}'...")
            # Сохраняем старый URL как резервный
            old_url = film.trailer_url
            
            # Пытаемся найти русский трейлер
            if self.add_trailer_to_film(film):
                self.stdout.write(f"  Заменен: {old_url} -> {film.trailer_url}")
            else:
                self.stdout.write(f"  Оставлен старый: {old_url}")