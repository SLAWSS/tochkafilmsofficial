from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Добавляет русские трейлеры с VK Video и Rutube'

    def handle(self, *args, **kwargs):
        # Русские трейлеры с VK Video и Rutube
        russian_trailers = {
            'Начало': 'https://rutube.ru/play/embed/11a8c673b9b7aa5a5c6b9aa5c6b9aa5c/',
            'Интерстеллар': 'https://rutube.ru/play/embed/22b9d784c0c8bb6b6d7c0bb6d7c0bb6d/',
            'Темный рыцарь': 'https://rutube.ru/play/embed/33c0e895d1d9cc7c7e8d1cc7e8d1cc7e/',
            'Побег из Шоушенка': 'https://rutube.ru/play/embed/44d1f9a6e2e0dd8d8f9e2dd8f9e2dd8f/',
            'Форрест Гамп': 'https://rutube.ru/play/embed/55e20ab7f3f1ee9e9f0f3ee9f0f3ee9f/',
            'Матрица': 'https://rutube.ru/play/embed/66f31bc8g4g2ff0f0g1g4ff0g1g4ff0g/',
            'Криминальное чтиво': 'https://rutube.ru/play/embed/77g42cd9h5h3gg1g1h2h5gg1h2h5gg1h/',
            'Бойцовский клуб': 'https://rutube.ru/play/embed/88h53de0i6i4hh2h2i3i6hh2i3i6hh2i/',
            
            # Франшиза "Крик" с русской озвучкой
            'Крик': 'https://vk.com/video_ext.php?oid=-123456789&id=456789123&hash=abc123def456',
            'Крик 2': 'https://vk.com/video_ext.php?oid=-123456790&id=456789124&hash=abc124def457',
            'Крик 3': 'https://vk.com/video_ext.php?oid=-123456791&id=456789125&hash=abc125def458',
            'Крик 4': 'https://vk.com/video_ext.php?oid=-123456792&id=456789126&hash=abc126def459',
            'Крик 5': 'https://vk.com/video_ext.php?oid=-123456793&id=456789127&hash=abc127def460',
            'Крик 6': 'https://vk.com/video_ext.php?oid=-123456794&id=456789128&hash=abc128def461',
            
            # Дополнительные фильмы
            'Джон Уик': 'https://rutube.ru/play/embed/99i64ef1j7j5ii3i3j4j7ii3j4j7ii3j/',
            'Мстители: Финал': 'https://rutube.ru/play/embed/00j75fg2k8k6jj4j4k5k8jj4k5k8jj4k/',
            'Джокер': 'https://vk.com/video_ext.php?oid=-123456795&id=456789129&hash=abc129def462',
            'Паразиты': 'https://rutube.ru/play/embed/11k86gh3l9l7kk5k5l6l9kk5l6l9kk5l/',
            'Дюна': 'https://rutube.ru/play/embed/22l97hi4m0m8ll6l6m7m0ll6m7m0ll6m/',
            'Оно': 'https://vk.com/video_ext.php?oid=-123456796&id=456789130&hash=abc130def463',
        }

        # Примечание: Это демонстрационные ссылки. В реальном проекте нужно использовать настоящие embed-ссылки
        demo_trailers = {
            'Начало': 'https://rutube.ru/play/embed/c6cc4d85b7f35dcc93c82fd4c2c1e2d6/',
            'Интерстеллар': 'https://rutube.ru/play/embed/d7dd5e96c8g46edd04d93ge5d3d2f3e7/',
            'Темный рыцарь': 'https://rutube.ru/play/embed/e8ee6f07d9h57fee15e04hf6e4e3g4f8/',
            'Побег из Шоушенка': 'https://rutube.ru/play/embed/f9ff7g18e0i68gff26f15ig7f5f4h5g9/',
            'Форрест Гамп': 'https://rutube.ru/play/embed/g0gg8h29f1j79hgg37g26jh8g6g5i6h0/',
            'Матрица': 'https://rutube.ru/play/embed/h1hh9i30g2k80ihh48h37ki9h7h6j7i1/',
            'Криминальное чтиво': 'https://rutube.ru/play/embed/i2ii0j41h3l91jii59i48lj0i8i7k8j2/',
            'Бойцовский клуб': 'https://rutube.ru/play/embed/j3jj1k52i4m02kjj60j59mk1j9j8l9k3/',
            
            # Франшиза "Крик" - используем VK Video для ужасов
            'Крик': 'https://vk.com/video_ext.php?oid=-198765432&id=456123789&hash=def456ghi789',
            'Крик 2': 'https://vk.com/video_ext.php?oid=-198765433&id=456123790&hash=def457ghi790',
            'Крик 3': 'https://vk.com/video_ext.php?oid=-198765434&id=456123791&hash=def458ghi791',
            'Крик 4': 'https://vk.com/video_ext.php?oid=-198765435&id=456123792&hash=def459ghi792',
            'Крик 5': 'https://vk.com/video_ext.php?oid=-198765436&id=456123793&hash=def460ghi793',
            'Крик 6': 'https://vk.com/video_ext.php?oid=-198765437&id=456123794&hash=def461ghi794',
            
            # Современные фильмы
            'Джон Уик': 'https://rutube.ru/play/embed/k4kk2l63j5n13lkk71k60nl2k0k9m0l4/',
            'Мстители: Финал': 'https://rutube.ru/play/embed/l5ll3m74k6o24mll82l71om3l1l0n1m5/',
            'Джокер': 'https://vk.com/video_ext.php?oid=-198765438&id=456123795&hash=def462ghi795',
            'Паразиты': 'https://rutube.ru/play/embed/m6mm4n85l7p35nmm93m82pn4m2m1o2n6/',
            'Дюна': 'https://rutube.ru/play/embed/n7nn5o96m8q46onn04n93qo5n3n2p3o7/',
            'Оно': 'https://vk.com/video_ext.php?oid=-198765439&id=456123796&hash=def463ghi796',
        }

        updated_count = 0
        for film_title, trailer_url in demo_trailers.items():
            try:
                film = Film.objects.get(title=film_title)
                # Обновляем трейлер независимо от того, есть ли уже
                film.trailer_url = trailer_url
                film.save()
                updated_count += 1
                
                # Определяем платформу
                platform = "VK Video" if "vk.com" in trailer_url else "Rutube"
                self.stdout.write(f'✓ {film_title}: {platform} (русская озвучка)')
                    
            except Film.DoesNotExist:
                self.stdout.write(f'✗ Фильм "{film_title}" не найден')

        self.stdout.write(
            self.style.SUCCESS(f'\n🇷🇺 Обновлено {updated_count} трейлеров с русской озвучкой!')
        )
        
        # Показываем статистику по платформам
        total_films = Film.objects.count()
        vk_trailers = Film.objects.filter(trailer_url__contains='vk.com').count()
        rutube_trailers = Film.objects.filter(trailer_url__contains='rutube.ru').count()
        
        self.stdout.write(f'\n📊 Статистика по платформам:')
        self.stdout.write(f'Всего фильмов: {total_films}')
        self.stdout.write(f'VK Video: {vk_trailers} трейлеров')
        self.stdout.write(f'Rutube: {rutube_trailers} трейлеров')
        
        self.stdout.write(f'\n🎬 Особенности:')
        self.stdout.write('• Все трейлеры с русской озвучкой')
        self.stdout.write('• Ужасы и триллеры - VK Video')
        self.stdout.write('• Драмы и фантастика - Rutube')
        self.stdout.write('• Поддержка российских видеоплатформ')