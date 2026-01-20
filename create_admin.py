from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Создает суперпользователя (админа)'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Имя пользователя')
        parser.add_argument('--email', type=str, default='admin@tochkafilms.ru', help='Email')
        parser.add_argument('--password', type=str, default='admin123', help='Пароль')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        
        # Проверяем, существует ли уже такой пользователь
        if User.objects.filter(username=username).exists():
            self.stdout.write(f"⚠️  Пользователь '{username}' уже существует")
            
            # Показываем информацию о существующем пользователе
            user = User.objects.get(username=username)
            self.stdout.write(f"📋 Информация о пользователе:")
            self.stdout.write(f"  Имя: {user.username}")
            self.stdout.write(f"  Email: {user.email}")
            self.stdout.write(f"  Суперпользователь: {'Да' if user.is_superuser else 'Нет'}")
            self.stdout.write(f"  Активен: {'Да' if user.is_active else 'Нет'}")
            self.stdout.write(f"  Дата создания: {user.date_joined}")
            
            # Предлагаем обновить пароль
            response = input("Обновить пароль? (y/n): ")
            if response.lower() == 'y':
                user.set_password(password)
                user.save()
                self.stdout.write(f"✅ Пароль обновлен для пользователя '{username}'")
            
            return
        
        # Создаем нового суперпользователя
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            self.stdout.write("=" * 50)
            self.stdout.write("👑 СУПЕРПОЛЬЗОВАТЕЛЬ СОЗДАН")
            self.stdout.write("=" * 50)
            self.stdout.write(f"✅ Имя пользователя: {username}")
            self.stdout.write(f"✅ Email: {email}")
            self.stdout.write(f"✅ Пароль: {password}")
            self.stdout.write("")
            self.stdout.write("🌐 Доступ к админке:")
            self.stdout.write("  URL: http://127.0.0.1:8000/admin/")
            self.stdout.write(f"  Логин: {username}")
            self.stdout.write(f"  Пароль: {password}")
            self.stdout.write("")
            self.stdout.write("🔧 Возможности админа:")
            self.stdout.write("  • Управление фильмами")
            self.stdout.write("  • Управление актерами")
            self.stdout.write("  • Управление категориями")
            self.stdout.write("  • Управление пользователями")
            self.stdout.write("  • Просмотр отзывов и уведомлений")
            
        except Exception as e:
            self.stdout.write(f"❌ Ошибка создания суперпользователя: {e}")

    def show_all_users(self):
        """Показывает всех пользователей"""
        users = User.objects.all().order_by('-date_joined')
        
        self.stdout.write("👥 ВСЕ ПОЛЬЗОВАТЕЛИ:")
        self.stdout.write("-" * 60)
        
        for user in users:
            status = "👑 Админ" if user.is_superuser else "👤 Пользователь"
            active = "✅ Активен" if user.is_active else "❌ Неактивен"
            
            self.stdout.write(f"{status} {user.username}")
            self.stdout.write(f"  Email: {user.email}")
            self.stdout.write(f"  Статус: {active}")
            self.stdout.write(f"  Создан: {user.date_joined.strftime('%d.%m.%Y %H:%M')}")
            self.stdout.write("")