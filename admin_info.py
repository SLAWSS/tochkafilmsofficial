from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Показывает информацию об админах'

    def handle(self, *args, **options):
        self.show_admin_info()

    def show_admin_info(self):
        """Показывает информацию об админах"""
        admins = User.objects.filter(is_superuser=True)
        
        self.stdout.write("=" * 60)
        self.stdout.write("👑 ИНФОРМАЦИЯ ОБ АДМИНИСТРАТОРАХ")
        self.stdout.write("=" * 60)
        
        if not admins.exists():
            self.stdout.write("❌ Администраторы не найдены")
            self.stdout.write("Создайте админа командой: python manage.py create_admin")
            return
        
        for admin in admins:
            self.stdout.write(f"👑 АДМИНИСТРАТОР: {admin.username}")
            self.stdout.write(f"  📧 Email: {admin.email or 'Не указан'}")
            self.stdout.write(f"  ✅ Активен: {'Да' if admin.is_active else 'Нет'}")
            self.stdout.write(f"  📅 Создан: {admin.date_joined.strftime('%d.%m.%Y %H:%M')}")
            self.stdout.write(f"  🔑 Последний вход: {admin.last_login.strftime('%d.%m.%Y %H:%M') if admin.last_login else 'Никогда'}")
            self.stdout.write("")
        
        self.stdout.write("🌐 ДОСТУП К АДМИНКЕ:")
        self.stdout.write("  URL: http://127.0.0.1:8000/admin/")
        self.stdout.write("  Логин: admin")
        self.stdout.write("  Пароль: admin123 (если не менялся)")
        self.stdout.write("")
        
        self.stdout.write("🔧 ВОЗМОЖНОСТИ АДМИНКИ:")
        self.stdout.write("  📽️  Управление фильмами (добавление, редактирование, удаление)")
        self.stdout.write("  🎭 Управление актерами (биографии, фото, связи с фильмами)")
        self.stdout.write("  📁 Управление категориями (создание, редактирование)")
        self.stdout.write("  👥 Управление пользователями (права, статусы)")
        self.stdout.write("  ⭐ Просмотр отзывов и рейтингов")
        self.stdout.write("  📢 Управление уведомлениями")
        self.stdout.write("  📊 Просмотр истории просмотров")
        self.stdout.write("")
        
        # Статистика
        from films.models import Film, Actor, Category, Review
        
        self.stdout.write("📊 СТАТИСТИКА САЙТА:")
        self.stdout.write(f"  🎬 Фильмов: {Film.objects.count()}")
        self.stdout.write(f"  🎭 Актеров: {Actor.objects.count()}")
        self.stdout.write(f"  📁 Категорий: {Category.objects.count()}")
        self.stdout.write(f"  ⭐ Отзывов: {Review.objects.count()}")
        self.stdout.write(f"  👥 Пользователей: {User.objects.count()}")
        self.stdout.write("")
        
        self.stdout.write("💡 ПОЛЕЗНЫЕ КОМАНДЫ:")
        self.stdout.write("  python manage.py create_admin --username newadmin --password newpass")
        self.stdout.write("  python manage.py changepassword admin")
        self.stdout.write("  python manage.py admin_info")