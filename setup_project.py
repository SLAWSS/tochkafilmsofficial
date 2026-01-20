from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Полная настройка проекта TochkaFilms'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🎬 Настройка проекта TochkaFilms'))
        self.stdout.write('=' * 50)
        
        # 1. Создаем тестовые данные
        self.stdout.write('1. Создание тестовых данных...')
        call_command('create_sample_data')
        
        # 2. Добавляем фильмы "Крик"
        self.stdout.write('\n2. Добавление франшизы "Крик"...')
        call_command('add_scream_movies')
        
        # 3. Создаем постеры
        self.stdout.write('\n3. Создание красивых постеров...')
        call_command('create_all_posters')
        
        # 4. Создаем дополнительные изображения
        self.stdout.write('\n4. Создание логотипа и иконок...')
        call_command('create_site_images')
        
        # 5. Добавляем русские трейлеры
        self.stdout.write('\n5. Добавление русских трейлеров...')
        call_command('add_russian_trailers')
        
        # 6. Создаем админа
        self.stdout.write('\n6. Создание администратора...')
        call_command('create_admin')
        
        # 7. Проверяем постеры
        self.stdout.write('\n7. Проверка постеров...')
        call_command('check_posters')
        
        # 8. Создаем тестовые уведомления
        self.stdout.write('\n8. Создание тестовых уведомлений...')
        call_command('create_notifications')
        
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('✅ Проект настроен успешно!'))
        self.stdout.write('\n🎉 Новые функции:')
        self.stdout.write('• Система рекомендаций')
        self.stdout.write('• Фильтрация и сортировка')
        self.stdout.write('• Топ фильмов по категориям')
        self.stdout.write('• История просмотров')
        self.stdout.write('• Уведомления')
        self.stdout.write('• Похожие фильмы')
        
        self.stdout.write('\n📋 Что делать дальше:')
        self.stdout.write('1. Запустите сервер: python manage.py runserver')
        self.stdout.write('2. Откройте: http://127.0.0.1:8000/')
        self.stdout.write('3. Админ-панель: http://127.0.0.1:8000/admin/ (admin/admin)')
        
        self.stdout.write('\n🔧 Команды для отладки:')
        self.stdout.write('- python manage.py test_media')
        self.stdout.write('- python manage.py check_russian_trailers')
        self.stdout.write('- python manage.py project_status')