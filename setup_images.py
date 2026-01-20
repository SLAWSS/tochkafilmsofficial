from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Создает все изображения для сайта'

    def handle(self, *args, **kwargs):
        self.stdout.write('Создание постеров для фильмов...')
        call_command('fix_posters')
        
        self.stdout.write('Создание дополнительных изображений...')
        call_command('create_site_images')
        
        self.stdout.write(self.style.SUCCESS('Все изображения созданы успешно!'))
        self.stdout.write('Теперь можно запустить сервер: python manage.py runserver')