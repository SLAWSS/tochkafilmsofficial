from django.core.management.base import BaseCommand
from films.models import Film
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import os
import time
import json


class Command(BaseCommand):
    help = 'Загружает постеры через API'

    def add_arguments(self, parser):
        parser.add_argument('--film-id', type=int, help='ID конкретного фильма')
        parser.add_argument('--search-term', type=str, help='Поисковый запрос')

    def handle(self, *args, **options):
        if options['film_id']:
            try:
                film = Film.objects.get(id=options['film_id'])
                self.fetch_poster_for_film(film)
            except Film.DoesNotExist:
                self.stdout.write(f"Фильм с ID {options['film_id']} не найден")
        elif options['search_term']:
            self.search_and_show_posters(options['search_term'])
        else:
            self.stdout.write("Используйте --film-id или --search-term")

    def search_omdb_api(self, title, year=None):
        """Поиск через OMDB API (бесплатный)"""
        # Для использования нужен API ключ с http://www.omdbapi.com/
        api_key = "YOUR_API_KEY"  # Замените на ваш ключ
        
        url = "http://www.omdbapi.com/"
        params = {
            'apikey': api_key,
            't': title,
            'type': 'movie'
        }
        
        if year:
            params['y'] = year
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('Response') == 'True':
                    return data.get('Poster')
        except Exception as e:
            self.stdout.write(f"Ошибка OMDB API: {e}")
        
        return None

    def search_tmdb_api(self, title, year=None):
        """Поиск через TMDB API (бесплатный)"""
        # Для использования нужен API ключ с https://www.themoviedb.org/settings/api
        api_key = "YOUR_API_KEY"  # Замените на ваш ключ
        
        search_url = "https://api.themoviedb.org/3/search/movie"
        params = {
            'api_key': api_key,
            'query': title,
            'language': 'ru-RU'
        }
        
        if year:
            params['year'] = year
        
        try:
            response = requests.get(search_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                if results:
                    poster_path = results[0].get('poster_path')
                    if poster_path:
                        return f"https://image.tmdb.org/t/p/w500{poster_path}"
        except Exception as e:
            self.stdout.write(f"Ошибка TMDB API: {e}")
        
        return None

    def get_free_poster_urls(self):
        """Возвращает словарь с бесплатными URL постеров"""
        return {
            "Тестовый фильм": "https://via.placeholder.com/300x450/2c3e50/ffffff?text=Test+Film",
            "Начало": "https://via.placeholder.com/300x450/1a1a1a/ffffff?text=Inception",
            "Интерстеллар": "https://via.placeholder.com/300x450/0f0f23/ffffff?text=Interstellar",
            "Темный рыцарь": "https://via.placeholder.com/300x450/000000/ffffff?text=Dark+Knight",
            # Можно добавить больше placeholder'ов или реальные URL
        }

    def download_poster(self, url):
        """Скачивает постер по URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                return response.content
            else:
                self.stdout.write(f"Ошибка загрузки: {response.status_code}")
                return None
        except Exception as e:
            self.stdout.write(f"Ошибка загрузки: {e}")
            return None

    def fetch_poster_for_film(self, film):
        """Загружает постер для фильма"""
        self.stdout.write(f"Ищу постер для '{film.title}' ({film.year})")
        
        # Сначала пробуем API
        poster_url = self.search_tmdb_api(film.title, film.year)
        if not poster_url:
            poster_url = self.search_omdb_api(film.title, film.year)
        
        # Если API не работают, используем заготовленные URL
        if not poster_url:
            free_urls = self.get_free_poster_urls()
            poster_url = free_urls.get(film.title)
        
        if not poster_url:
            self.stdout.write(f"⚠️  Постер для '{film.title}' не найден")
            return False
        
        # Скачиваем постер
        poster_data = self.download_poster(poster_url)
        if not poster_data:
            return False
        
        try:
            # Создаем временный файл
            temp_file = NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_file.write(poster_data)
            temp_file.close()
            
            # Сохраняем в модель
            filename = f"{film.title.lower().replace(' ', '_').replace(':', '')}_api_poster.jpg"
            with open(temp_file.name, 'rb') as f:
                film.poster.save(filename, File(f))
            
            # Удаляем временный файл
            os.unlink(temp_file.name)
            
            self.stdout.write(f"✅ Постер добавлен для '{film.title}'")
            return True
            
        except Exception as e:
            self.stdout.write(f"❌ Ошибка сохранения постера: {e}")
            return False

    def search_and_show_posters(self, search_term):
        """Показывает найденные постеры"""
        self.stdout.write(f"Поиск постеров для: {search_term}")
        
        tmdb_url = self.search_tmdb_api(search_term)
        omdb_url = self.search_omdb_api(search_term)
        
        if tmdb_url:
            self.stdout.write(f"TMDB: {tmdb_url}")
        if omdb_url:
            self.stdout.write(f"OMDB: {omdb_url}")
        
        if not tmdb_url and not omdb_url:
            self.stdout.write("Постеры не найдены")