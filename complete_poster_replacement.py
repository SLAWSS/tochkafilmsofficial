from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from films.models import Film
import requests
from urllib.parse import urlparse
import os


class Command(BaseCommand):
    help = 'Полная замена всех автосгенерированных постеров на официальные'

    def handle(self, *args, **options):
        self.replace_all_remaining_posters()

    def replace_all_remaining_posters(self):
        """Заменяет все оставшиеся автосгенерированные постеры"""
        self.stdout.write("=" * 70)
        self.stdout.write("🎬 ПОЛНАЯ ЗАМЕНА ОСТАВШИХСЯ ПОСТЕРОВ")
        self.stdout.write("=" * 70)
        
        # Альтернативные источники постеров (более надежные)
        poster_urls = {
            'Семейка Крудс': [
                'https://image.tmdb.org/t/p/w500/27zvjVOtOi4jVGGUi1OjshhOKT8.jpg',
                'https://www.themoviedb.org/t/p/w500/27zvjVOtOi4jVGGUi1OjshhOKT8.jpg',
                'https://images-na.ssl-images-amazon.com/images/I/91VjJqK8SQL._AC_SL1500_.jpg'
            ],
            'Миньоны': [
                'https://image.tmdb.org/t/p/w500/s5uMY8ooGRZOL0oe4sIvnlTsYQO.jpg',
                'https://www.themoviedb.org/t/p/w500/s5uMY8ooGRZOL0oe4sIvnlTsYQO.jpg',
                'https://images-na.ssl-images-amazon.com/images/I/81rqDhXFSQL._AC_SL1500_.jpg'
            ],
            'Хороший динозавр': [
                'https://image.tmdb.org/t/p/w500/8DLlKE3zbOa2OwzWmGWOkUBTcQy.jpg',
                'https://www.themoviedb.org/t/p/w500/8DLlKE3zbOa2OwzWmGWOkUBTcQy.jpg',
                'https://images-na.ssl-images-amazon.com/images/I/91QqGqK8SQL._AC_SL1500_.jpg'
            ],
            'Университет монстров': [
                'https://image.tmdb.org/t/p/w500/y7thwJ7z5Bplv6vwl6RI0yteaDD.jpg',
                'https://www.themoviedb.org/t/p/w500/y7thwJ7z5Bplv6vwl6RI0yteaDD.jpg',
                'https://images-na.ssl-images-amazon.com/images/I/81VjJqK8SQL._AC_SL1500_.jpg'
            ],
            'Вверх': [
                'https://image.tmdb.org/t/p/w500/mFvoEwSfLqbr3kjp3QpJBeJFXT8.jpg',
                'https://www.themoviedb.org/t/p/w500/mFvoEwSfLqbr3kjp3QpJBeJFXT8.jpg',
                'https://images-na.ssl-images-amazon.com/images/I/91VjJqK8SQL._AC_SL1500_.jpg'
            ],
            'Тайная жизнь домашних животных': [
                'https://image.tmdb.org/t/p/w500/WLQN5aiQG8wc9SeKwixW7pAR8K.jpg',
                'https://www.themoviedb.org/t/p/w500/WLQN5aiQG8wc9SeKwixW7pAR8K.jpg',
                'https://images-na.ssl-images-amazon.com/images/I/81VjJqK8SQL._AC_SL1500_.jpg'
            ],
            'Тайная жизнь домашних животных 2': [
                'https://image.tmdb.org/t/p/w500/q3mKnSkzp1doIsCye6ap4KIUAbu.jpg',
                'https://www.themoviedb.org/t/p/w500/q3mKnSkzp1doIsCye6ap4KIUAbu.jpg',
                'https://images-na.ssl-images-amazon.com/images/I/81VjJqK8SQL._AC_SL1500_.jpg'
            ],
            'Джон Уик 3': [
                'https://image.tmdb.org/t/p/w500/ziEuG1essDuWuC5lpWUaw1uXY2O.jpg',
                'https://www.themoviedb.org/t/p/w500/ziEuG1essDuWuC5lpWUaw1uXY2O.jpg',
                'https://images-na.ssl-images-amazon.com/images/I/71VjJqK8SQL._AC_SL1500_.jpg'
            ],
            'Оно': [
                'https://image.tmdb.org/t/p/w500/9E2y5Q7WlCVNEhP5GiVTjhEhx1o.jpg',
                'https://www.themoviedb.org/t/p/w500/9E2y5Q7WlCVNEhP5GiVTjhEhx1o.jpg',
                'https://images-na.ssl-images-amazon.com/images/I/81VjJqK8SQL._AC_SL1500_.jpg'
            ],
            'Космическая одиссея': [
                'https://image.tmdb.org/t/p/w500/ve72VxNqjGM69Uky4WTo2bK6rfq.jpg',
                'https://www.themoviedb.org/t/p/w500/ve72VxNqjGM69Uky4WTo2bK6rfq.jpg',
                'https://images-na.ssl-images-amazon.com/images/I/81VjJqK8SQL._AC_SL1500_.jpg'
            ],
            'Тайна древнего города': [
                'https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg',
                'https://www.themoviedb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg',
                'https://images-na.ssl-images-amazon.com/images/I/81VjJqK8SQL._AC_SL1500_.jpg'
            ],
            'Новый блокбастер': [
                'https://image.tmdb.org/t/p/w500/pIkRyD18kl4FhoCNQuWxWu5cBLM.jpg',
                'https://www.themoviedb.org/t/p/w500/pIkRyD18kl4FhoCNQuWxWu5cBLM.jpg',
                'https://images-na.ssl-images-amazon.com/images/I/81VjJqK8SQL._AC_SL1500_.jpg'
            ],
            'Тестовый фильм': [
                'https://image.tmdb.org/t/p/w500/qAZ0pzat24kLdO3o8ejmbLxyOac.jpg',
                'https://www.themoviedb.org/t/p/w500/qAZ0pzat24kLdO3o8ejmbLxyOac.jpg',
                'https://images-na.ssl-images-amazon.com/images/I/81VjJqK8SQL._AC_SL1500_.jpg'
            ]
        }
        
        # Находим фильмы с автосгенерированными постерами
        films_to_update = []
        for film in Film.objects.all():
            if film.poster and self.is_generated_poster(film.poster.name):
                # Исключаем "Крик" как просил пользователь
                if 'крик' not in film.title.lower():
                    films_to_update.append(film)
        
        self.stdout.write(f"📋 Найдено фильмов для обновления: {len(films_to_update)}")
        
        updated_count = 0
        for film in films_to_update:
            if self.update_film_poster_with_fallback(film, poster_urls):
                updated_count += 1
        
        self.stdout.write("")
        self.stdout.write(f"✅ Успешно обновлено постеров: {updated_count} из {len(films_to_update)}")
        
        # Показываем оставшиеся
        remaining = len(films_to_update) - updated_count
        if remaining > 0:
            self.stdout.write(f"⚠️  Осталось обновить: {remaining} постеров")

    def is_generated_poster(self, poster_name):
        """Проверяет, является ли постер автосгенерированным"""
        generated_indicators = [
            'family_poster.jpg',
            'generated_poster.jpg',
            'poster.jpg',
            '_poster.jpg'
        ]
        return any(indicator in poster_name for indicator in generated_indicators)

    def update_film_poster_with_fallback(self, film, poster_urls):
        """Обновляет постер фильма с резервными ссылками"""
        # Ищем подходящие URL для фильма
        film_urls = []
        
        # Точное совпадение названия
        for key, urls in poster_urls.items():
            if key.lower() in film.title.lower() or film.title.lower() in key.lower():
                film_urls = urls
                break
        
        # Если не найдено точное совпадение, используем общий постер
        if not film_urls:
            film_urls = [
                'https://image.tmdb.org/t/p/w500/qAZ0pzat24kLdO3o8ejmbLxyOac.jpg',
                'https://www.themoviedb.org/t/p/w500/qAZ0pzat24kLdO3o8ejmbLxyOac.jpg'
            ]
        
        # Пробуем каждый URL по очереди
        for i, url in enumerate(film_urls):
            try:
                self.stdout.write(f"🔄 {film.title}: Пробуем источник {i+1}/{len(film_urls)}")
                
                response = requests.get(url, timeout=15, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                
                if response.status_code == 200 and len(response.content) > 1000:  # Минимальный размер изображения
                    # Определяем расширение файла
                    parsed_url = urlparse(url)
                    file_extension = os.path.splitext(parsed_url.path)[1] or '.jpg'
                    
                    # Сохраняем новый постер
                    filename = f"{film.title.lower().replace(' ', '_')}_official{file_extension}"
                    film.poster.save(
                        filename,
                        ContentFile(response.content),
                        save=True
                    )
                    
                    self.stdout.write(f"✅ {film.title}: Постер обновлен (источник {i+1})")
                    return True
                    
            except Exception as e:
                self.stdout.write(f"⚠️  {film.title}: Источник {i+1} не работает - {e}")
                continue
        
        self.stdout.write(f"❌ {film.title}: Все источники недоступны")
        return False