from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Создает только постеры для фильмов'

    def handle(self, *args, **kwargs):
        self.stdout.write('Создание постеров для фильмов...')
        call_command('fix_posters')
        
        self.stdout.write(self.style.SUCCESS('Постеры созданы успешно!'))
        self.stdout.write('Проверить результат: python manage.py check_posters')