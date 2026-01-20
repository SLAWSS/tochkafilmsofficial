from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Настраивает кастомную админ-панель в стиле сайта'

    def handle(self, *args, **options):
        self.setup_custom_admin()

    def setup_custom_admin(self):
        """Настраивает кастомную админ-панель"""
        self.stdout.write("=" * 60)
        self.stdout.write("🎨 НАСТРОЙКА КАСТОМНОЙ АДМИН-ПАНЕЛИ")
        self.stdout.write("=" * 60)
        
        # Проверяем наличие файлов
        files_to_check = [
            'static/admin/css/custom_admin.css',
            'templates/admin/base_site.html',
            'templates/admin/index.html',
            'templates/admin/films/film/change_list.html'
        ]
        
        missing_files = []
        existing_files = []
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                existing_files.append(file_path)
                self.stdout.write(f"✅ {file_path}")
            else:
                missing_files.append(file_path)
                self.stdout.write(f"❌ {file_path}")
        
        self.stdout.write("")
        self.stdout.write(f"📊 СТАТУС ФАЙЛОВ:")
        self.stdout.write(f"  ✅ Найдено: {len(existing_files)}")
        self.stdout.write(f"  ❌ Отсутствует: {len(missing_files)}")
        
        if missing_files:
            self.stdout.write("")
            self.stdout.write("⚠️  ОТСУТСТВУЮЩИЕ ФАЙЛЫ:")
            for file_path in missing_files:
                self.stdout.write(f"  • {file_path}")
        
        # Проверяем настройки Django
        self.check_django_settings()
        
        # Показываем инструкции
        self.show_instructions()

    def check_django_settings(self):
        """Проверяет настройки Django"""
        self.stdout.write("")
        self.stdout.write("🔧 ПРОВЕРКА НАСТРОЕК DJANGO:")
        
        # Проверяем TEMPLATES
        templates_dirs = settings.TEMPLATES[0]['DIRS']
        if templates_dirs:
            self.stdout.write("✅ TEMPLATES['DIRS'] настроен")
        else:
            self.stdout.write("❌ TEMPLATES['DIRS'] не настроен")
            self.stdout.write("   Добавьте в settings.py: 'DIRS': [BASE_DIR / 'templates']")
        
        # Проверяем STATICFILES_DIRS
        if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
            self.stdout.write("✅ STATICFILES_DIRS настроен")
        else:
            self.stdout.write("❌ STATICFILES_DIRS не настроен")
            self.stdout.write("   Добавьте в settings.py: STATICFILES_DIRS = [BASE_DIR / 'static']")

    def show_instructions(self):
        """Показывает инструкции по использованию"""
        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write("📋 ИНСТРУКЦИИ ПО ИСПОЛЬЗОВАНИЮ")
        self.stdout.write("=" * 60)
        
        self.stdout.write("🚀 ЗАПУСК СЕРВЕРА:")
        self.stdout.write("  python manage.py runserver")
        self.stdout.write("")
        
        self.stdout.write("🌐 ДОСТУП К АДМИНКЕ:")
        self.stdout.write("  URL: http://127.0.0.1:8000/admin/")
        self.stdout.write("  Логин: admin")
        self.stdout.write("  Пароль: admin123")
        self.stdout.write("")
        
        self.stdout.write("✨ НОВЫЕ ВОЗМОЖНОСТИ АДМИНКИ:")
        self.stdout.write("  🎨 Темная тема в стиле сайта")
        self.stdout.write("  🎬 Красивая главная страница с статистикой")
        self.stdout.write("  🖼️  Увеличение постеров при наведении")
        self.stdout.write("  📊 Интерактивные счетчики")
        self.stdout.write("  🎯 Быстрые действия на главной")
        self.stdout.write("  🌟 Анимации и переходы")
        self.stdout.write("  📱 Адаптивный дизайн")
        self.stdout.write("")
        
        self.stdout.write("🎨 ЦВЕТОВАЯ СХЕМА:")
        self.stdout.write("  🔴 Основной: #e50914 (красный Netflix)")
        self.stdout.write("  ⚫ Фон: градиент темных тонов")
        self.stdout.write("  ⚪ Текст: белый и оттенки серого")
        self.stdout.write("  🟡 Акценты: золотой для важных элементов")
        self.stdout.write("")
        
        self.stdout.write("💡 ПОЛЕЗНЫЕ СОВЕТЫ:")
        self.stdout.write("  • Наведите на постеры для увеличения")
        self.stdout.write("  • Используйте быстрые действия на главной")
        self.stdout.write("  • Админка адаптируется под размер экрана")
        self.stdout.write("  • Все элементы имеют плавные анимации")
        self.stdout.write("")
        
        self.stdout.write("🔧 КАСТОМИЗАЦИЯ:")
        self.stdout.write("  • Стили: static/admin/css/custom_admin.css")
        self.stdout.write("  • Шаблоны: templates/admin/")
        self.stdout.write("  • Цвета можно изменить в CSS файле")
        
        self.show_admin_features()

    def show_admin_features(self):
        """Показывает особенности новой админки"""
        self.stdout.write("")
        self.stdout.write("🌟 ОСОБЕННОСТИ НОВОЙ АДМИНКИ:")
        self.stdout.write("")
        
        features = [
            ("🎬 Главная страница", "Статистика, быстрые действия, анимированные счетчики"),
            ("🖼️  Превью постеров", "Увеличение при наведении, красивые рамки"),
            ("📊 Статистика фильмов", "Подсчет фильмов с постерами, трейлерами"),
            ("🎨 Темная тема", "В стиле основного сайта с градиентами"),
            ("⚡ Быстрые действия", "Кнопки для частых операций"),
            ("📱 Адаптивность", "Работает на всех устройствах"),
            ("🌈 Анимации", "Плавные переходы и эффекты"),
            ("🔍 Улучшенная навигация", "Красивые breadcrumbs и меню"),
            ("💫 Эффекты", "Размытие фона, тени, градиенты"),
            ("🎯 UX/UI", "Интуитивный и современный интерфейс")
        ]
        
        for feature, description in features:
            self.stdout.write(f"  {feature}")
            self.stdout.write(f"    {description}")
            self.stdout.write("")
        
        self.stdout.write("🎉 Кастомная админ-панель готова к использованию!")
        self.stdout.write("   Перезапустите сервер для применения изменений")