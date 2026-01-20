from django.core.management.base import BaseCommand
from django.conf import settings
import os
import shutil
from PIL import Image
import zipfile


class Command(BaseCommand):
    help = 'Подготавливает проект для загрузки на GitHub (сжимает файлы, очищает кэш)'

    def add_arguments(self, parser):
        parser.add_argument('--compress-images', action='store_true', help='Сжать изображения')
        parser.add_argument('--clean-cache', action='store_true', help='Очистить кэш')
        parser.add_argument('--create-gitignore', action='store_true', help='Создать .gitignore')
        parser.add_argument('--all', action='store_true', help='Выполнить все операции')

    def handle(self, *args, **options):
        if options['all']:
            options['compress_images'] = True
            options['clean_cache'] = True
            options['create_gitignore'] = True

        self.stdout.write("=" * 60)
        self.stdout.write("📦 ПОДГОТОВКА ПРОЕКТА ДЛЯ GITHUB")
        self.stdout.write("=" * 60)

        if options['create_gitignore']:
            self.create_gitignore()

        if options['clean_cache']:
            self.clean_cache()

        if options['compress_images']:
            self.compress_images()

        self.show_project_size()
        self.show_github_tips()

    def create_gitignore(self):
        """Создает .gitignore файл"""
        self.stdout.write("📝 Создание .gitignore...")
        
        gitignore_content = """# Django
*.log
*.pot
*.pyc
__pycache__/
local_settings.py
db.sqlite3
db.sqlite3-journal

# Media files (слишком большие для GitHub)
media/
!media/.gitkeep

# Static files (будут собраны заново)
staticfiles/
collected_static/

# Environment variables
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Python
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Testing
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# Backup files
*.bak
*.backup
*.old

# Temporary files
*.tmp
*.temp
"""
        
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        
        self.stdout.write("✅ .gitignore создан")

    def clean_cache(self):
        """Очищает кэш и временные файлы"""
        self.stdout.write("🧹 Очистка кэша и временных файлов...")
        
        cleaned_count = 0
        
        # Очищаем __pycache__
        for root, dirs, files in os.walk('.'):
            if '__pycache__' in dirs:
                pycache_path = os.path.join(root, '__pycache__')
                try:
                    shutil.rmtree(pycache_path)
                    cleaned_count += 1
                except Exception as e:
                    self.stdout.write(f"⚠️  Не удалось удалить {pycache_path}: {e}")
        
        # Очищаем .pyc файлы
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.pyc'):
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        cleaned_count += 1
                    except Exception as e:
                        self.stdout.write(f"⚠️  Не удалось удалить {file_path}: {e}")
        
        self.stdout.write(f"✅ Очищено {cleaned_count} файлов кэша")

    def compress_images(self):
        """Сжимает изображения для экономии места"""
        self.stdout.write("🖼️  Сжатие изображений...")
        
        media_root = getattr(settings, 'MEDIA_ROOT', 'media')
        if not os.path.exists(media_root):
            self.stdout.write("⚠️  Папка media не найдена")
            return
        
        compressed_count = 0
        total_saved = 0
        
        for root, dirs, files in os.walk(media_root):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    file_path = os.path.join(root, file)
                    try:
                        original_size = os.path.getsize(file_path)
                        
                        # Открываем и сжимаем изображение
                        with Image.open(file_path) as img:
                            # Конвертируем в RGB если нужно
                            if img.mode in ('RGBA', 'LA', 'P'):
                                img = img.convert('RGB')
                            
                            # Уменьшаем размер если слишком большое
                            max_size = (800, 1200)  # Максимальный размер для постеров
                            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                            
                            # Сохраняем с сжатием
                            img.save(file_path, 'JPEG', quality=85, optimize=True)
                        
                        new_size = os.path.getsize(file_path)
                        saved = original_size - new_size
                        
                        if saved > 0:
                            total_saved += saved
                            compressed_count += 1
                            self.stdout.write(f"  📉 {file}: сэкономлено {self.format_size(saved)}")
                    
                    except Exception as e:
                        self.stdout.write(f"⚠️  Ошибка сжатия {file_path}: {e}")
        
        self.stdout.write(f"✅ Сжато {compressed_count} изображений")
        self.stdout.write(f"💾 Сэкономлено: {self.format_size(total_saved)}")

    def show_project_size(self):
        """Показывает размер проекта"""
        self.stdout.write("")
        self.stdout.write("📊 РАЗМЕР ПРОЕКТА:")
        
        total_size = 0
        file_count = 0
        
        # Подсчитываем размер всех файлов (кроме .git)
        for root, dirs, files in os.walk('.'):
            # Исключаем .git папку
            if '.git' in dirs:
                dirs.remove('.git')
            
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    total_size += size
                    file_count += 1
                except:
                    pass
        
        self.stdout.write(f"📁 Всего файлов: {file_count}")
        self.stdout.write(f"📦 Общий размер: {self.format_size(total_size)}")
        
        # Размер по папкам
        folder_sizes = {}
        for item in os.listdir('.'):
            if os.path.isdir(item) and item != '.git':
                folder_size = self.get_folder_size(item)
                folder_sizes[item] = folder_size
        
        # Сортируем по размеру
        sorted_folders = sorted(folder_sizes.items(), key=lambda x: x[1], reverse=True)
        
        self.stdout.write("")
        self.stdout.write("📂 Размер по папкам:")
        for folder, size in sorted_folders[:10]:  # Топ 10
            self.stdout.write(f"  {folder}: {self.format_size(size)}")

    def get_folder_size(self, folder_path):
        """Получает размер папки"""
        total_size = 0
        try:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        total_size += os.path.getsize(file_path)
                    except:
                        pass
        except:
            pass
        return total_size

    def format_size(self, size_bytes):
        """Форматирует размер в читаемый вид"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"

    def show_github_tips(self):
        """Показывает советы для GitHub"""
        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write("🚀 СОВЕТЫ ДЛЯ ЗАГРУЗКИ НА GITHUB")
        self.stdout.write("=" * 60)
        
        self.stdout.write("📋 КОМАНДЫ GIT:")
        self.stdout.write("  git init")
        self.stdout.write("  git add .")
        self.stdout.write("  git commit -m 'Initial commit: TochkaFilms Django project'")
        self.stdout.write("  git branch -M main")
        self.stdout.write("  git remote add origin https://github.com/username/tochkafilms.git")
        self.stdout.write("  git push -u origin main")
        self.stdout.write("")
        
        self.stdout.write("💡 РЕКОМЕНДАЦИИ:")
        self.stdout.write("  • Создайте репозиторий на GitHub сначала")
        self.stdout.write("  • Замените 'username' на ваш GitHub username")
        self.stdout.write("  • Медиафайлы исключены из .gitignore (слишком большие)")
        self.stdout.write("  • База данных db.sqlite3 тоже исключена")
        self.stdout.write("  • После клонирования нужно будет:")
        self.stdout.write("    - python manage.py migrate")
        self.stdout.write("    - python manage.py create_admin")
        self.stdout.write("    - python manage.py add_family_films")
        self.stdout.write("")
        
        self.stdout.write("📝 СОЗДАЙТЕ README.md:")
        readme_content = '''# TochkaFilms - Django Movie Portal

🎬 Современный веб-портал для просмотра фильмов с удобным интерфейсом и богатым функционалом.

## ✨ Возможности

- 📽️ Каталог из 143+ фильмов с постерами и трейлерами
- 🎭 База актеров с биографиями и фотографиями  
- 📁 Категории и жанры фильмов
- ⭐ Система рейтингов и отзывов
- 👤 Личные кабинеты пользователей
- 📱 Адаптивный дизайн
- 🔍 Поиск и фильтрация

## 🚀 Быстрый старт

```bash
# Клонирование
git clone https://github.com/username/tochkafilms.git
cd tochkafilms

# Установка зависимостей
pip install -r requirements.txt

# Миграции
python manage.py migrate

# Создание админа
python manage.py create_admin

# Добавление фильмов
python manage.py add_family_films

# Запуск сервера
python manage.py runserver
```

## 📊 Статистика

- 🎬 143 фильма
- 🎭 6 актеров  
- 📁 16 категорий
- 100% покрытие постерами

## 🛠️ Технологии

- Django 4.x
- SQLite
- Bootstrap
- Pillow (обработка изображений)
'''
        
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        self.stdout.write("✅ README.md создан")
        self.stdout.write("")
        self.stdout.write("🎉 Проект готов к загрузке на GitHub!")