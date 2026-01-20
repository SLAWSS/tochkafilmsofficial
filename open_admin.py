from django.core.management.base import BaseCommand
import webbrowser
import time


class Command(BaseCommand):
    help = 'Открывает админку в браузере'

    def add_arguments(self, parser):
        parser.add_argument('--port', type=int, default=8000, help='Порт сервера')
        parser.add_argument('--no-browser', action='store_true', help='Не открывать браузер')

    def handle(self, *args, **options):
        port = options['port']
        admin_url = f"http://127.0.0.1:{port}/admin/"
        
        self.stdout.write("=" * 60)
        self.stdout.write("🌐 ДОСТУП К АДМИНКЕ TOCHKAFILMS")
        self.stdout.write("=" * 60)
        
        self.stdout.write(f"🔗 URL: {admin_url}")
        self.stdout.write("👤 Логин: admin")
        self.stdout.write("🔑 Пароль: admin123")
        self.stdout.write("")
        
        self.stdout.write("📋 РАЗДЕЛЫ АДМИНКИ:")
        self.stdout.write("  🎬 Фильмы - управление фильмами, постерами, трейлерами")
        self.stdout.write("  🎭 Актеры - биографии, фото, связи с фильмами")
        self.stdout.write("  📁 Категории - жанры и категории фильмов")
        self.stdout.write("  👥 Пользователи - управление аккаунтами")
        self.stdout.write("  ⭐ Отзывы - модерация отзывов и рейтингов")
        self.stdout.write("  📊 История - просмотры пользователей")
        self.stdout.write("  📢 Уведомления - системные сообщения")
        self.stdout.write("")
        
        self.stdout.write("✨ НОВЫЕ ВОЗМОЖНОСТИ АДМИНКИ:")
        self.stdout.write("  • Превью постеров и фото актеров")
        self.stdout.write("  • Быстрые ссылки на трейлеры")
        self.stdout.write("  • Счетчики фильмов по категориям")
        self.stdout.write("  • Массовые действия с уведомлениями")
        self.stdout.write("  • Улучшенная фильтрация и поиск")
        self.stdout.write("")
        
        if not options['no_browser']:
            self.stdout.write("🚀 Открываю админку в браузере...")
            try:
                webbrowser.open(admin_url)
                self.stdout.write("✅ Браузер открыт!")
            except Exception as e:
                self.stdout.write(f"❌ Не удалось открыть браузер: {e}")
                self.stdout.write(f"Откройте вручную: {admin_url}")
        
        self.stdout.write("")
        self.stdout.write("💡 ПОЛЕЗНЫЕ СОВЕТЫ:")
        self.stdout.write("  • Используйте фильтры для быстрого поиска")
        self.stdout.write("  • Кликайте на превью для увеличения")
        self.stdout.write("  • Используйте массовые действия для экономии времени")
        self.stdout.write("  • Проверяйте связи между фильмами и актерами")
        
        # Показываем статистику
        self.show_quick_stats()

    def show_quick_stats(self):
        """Показывает быструю статистику"""
        try:
            from films.models import Film, Actor, Category, Review
            from django.contrib.auth.models import User
            
            self.stdout.write("")
            self.stdout.write("📊 БЫСТРАЯ СТАТИСТИКА:")
            self.stdout.write(f"  🎬 Фильмов: {Film.objects.count()}")
            self.stdout.write(f"  🎭 Актеров: {Actor.objects.count()}")
            self.stdout.write(f"  📁 Категорий: {Category.objects.count()}")
            self.stdout.write(f"  ⭐ Отзывов: {Review.objects.count()}")
            self.stdout.write(f"  👥 Пользователей: {User.objects.count()}")
            
            # Последние добавления
            latest_film = Film.objects.order_by('-created_at').first()
            if latest_film:
                self.stdout.write(f"  🆕 Последний фильм: {latest_film.title} ({latest_film.year})")
            
        except Exception as e:
            self.stdout.write(f"  ⚠️  Не удалось загрузить статистику: {e}")