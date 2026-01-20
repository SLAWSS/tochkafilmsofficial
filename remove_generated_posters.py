from django.core.management.base import BaseCommand
from films.models import Film
import os


class Command(BaseCommand):
    help = 'Удаляет автосгенерированные постеры (лучше без постера, чем с самодельным)'

    def add_arguments(self, parser):
        parser.add_argument('--confirm', action='store_true', help='Подтвердить удаление')

    def handle(self, *args, **options):
        if options['confirm']:
            self.remove_generated_posters()
        else:
            self.show_preview()

    def show_preview(self):
        """Показывает предварительный просмотр"""
        self.stdout.write("=" * 70)
        self.stdout.write("🔍 ПРЕДВАРИТЕЛЬНЫЙ ПРОСМОТР УДАЛЕНИЯ")
        self.stdout.write("=" * 70)
        
        films_to_clean = []
        for film in Film.objects.all():
            if film.poster and self.is_generated_poster(film.poster.name):
                # Исключаем "Крик" как просил пользователь
                if 'крик' not in film.title.lower():
                    films_to_clean.append(film)
        
        self.stdout.write(f"📋 Найдено фильмов с автосгенерированными постерами: {len(films_to_clean)}")
        self.stdout.write("")
        self.stdout.write("Будут удалены постеры у следующих фильмов:")
        
        for film in films_to_clean:
            self.stdout.write(f"  • {film.title} ({film.year}) - {film.poster.name}")
        
        self.stdout.write("")
        self.stdout.write("💡 ОБОСНОВАНИЕ:")
        self.stdout.write("   Лучше оставить фильм без постера, чем с самодельным")
        self.stdout.write("   Автосгенерированные постеры выглядят непрофессионально")
        self.stdout.write("   В будущем можно добавить настоящие официальные постеры")
        self.stdout.write("")
        self.stdout.write("🚀 Для выполнения запустите:")
        self.stdout.write("   python manage.py remove_generated_posters --confirm")

    def remove_generated_posters(self):
        """Удаляет автосгенерированные постеры"""
        self.stdout.write("=" * 70)
        self.stdout.write("🗑️  УДАЛЕНИЕ АВТОСГЕНЕРИРОВАННЫХ ПОСТЕРОВ")
        self.stdout.write("=" * 70)
        
        films_to_clean = []
        for film in Film.objects.all():
            if film.poster and self.is_generated_poster(film.poster.name):
                # Исключаем "Крик" как просил пользователь
                if 'крик' not in film.title.lower():
                    films_to_clean.append(film)
        
        self.stdout.write(f"📋 Найдено фильмов для очистки: {len(films_to_clean)}")
        
        cleaned_count = 0
        for film in films_to_clean:
            try:
                # Удаляем файл постера
                if film.poster:
                    poster_path = film.poster.path
                    if os.path.exists(poster_path):
                        os.remove(poster_path)
                    
                    # Очищаем поле в базе данных
                    film.poster = None
                    film.save()
                
                self.stdout.write(f"✅ {film.title}: Автосгенерированный постер удален")
                cleaned_count += 1
                
            except Exception as e:
                self.stdout.write(f"❌ {film.title}: Ошибка - {e}")
        
        self.stdout.write("")
        self.stdout.write(f"✅ Успешно очищено: {cleaned_count} из {len(films_to_clean)}")
        
        # Финальная статистика
        self.show_final_statistics()

    def is_generated_poster(self, poster_name):
        """Проверяет, является ли постер автосгенерированным"""
        generated_indicators = [
            'family_poster.jpg',
            'generated_poster.jpg',
            'poster.jpg',
            '_poster.jpg'
        ]
        return any(indicator in poster_name for indicator in generated_indicators)

    def show_final_statistics(self):
        """Показывает финальную статистику"""
        self.stdout.write("")
        self.stdout.write("=" * 70)
        self.stdout.write("📊 ФИНАЛЬНАЯ СТАТИСТИКА ПОСТЕРОВ")
        self.stdout.write("=" * 70)
        
        total_films = Film.objects.count()
        films_with_posters = Film.objects.exclude(poster='').exclude(poster=None).count()
        films_without_posters = total_films - films_with_posters
        
        # Проверяем оставшиеся автосгенерированные
        remaining_generated = 0
        official_posters = 0
        
        for film in Film.objects.all():
            if film.poster:
                if self.is_generated_poster(film.poster.name):
                    remaining_generated += 1
                else:
                    official_posters += 1
        
        self.stdout.write(f"🎬 Всего фильмов: {total_films}")
        self.stdout.write(f"✅ С официальными постерами: {official_posters}")
        self.stdout.write(f"❌ Без постеров: {films_without_posters}")
        self.stdout.write(f"⚠️  С автосгенерированными: {remaining_generated}")
        self.stdout.write("")
        
        if remaining_generated == 0:
            self.stdout.write("🎉 ОТЛИЧНО! Все автосгенерированные постеры удалены!")
            self.stdout.write("   Теперь у фильмов либо официальные постеры, либо их нет вовсе")
        
        self.stdout.write("")
        self.stdout.write("💡 РЕКОМЕНДАЦИИ:")
        self.stdout.write("   • Для фильмов без постеров можно найти официальные изображения")
        self.stdout.write("   • Используйте только качественные официальные постеры")
        self.stdout.write("   • Избегайте самодельных изображений")
        self.stdout.write("")
        self.stdout.write("🌐 Проверить результат:")
        self.stdout.write("   • Админка: http://127.0.0.1:8000/admin/")
        self.stdout.write("   • Сайт: http://127.0.0.1:8000/")