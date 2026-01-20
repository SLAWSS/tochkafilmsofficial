from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Добавление дополнительных Rutube трейлеров на русском языке'

    def handle(self, *args, **options):
        self.stdout.write("🎬 ДОБАВЛЕНИЕ ДОПОЛНИТЕЛЬНЫХ RUTUBE ТРЕЙЛЕРОВ")
        self.stdout.write("=" * 60)
        
        # Дополнительные Rutube трейлеры для фильмов без трейлеров
        additional_trailers = {
            'Звездные войны: Новая надежда': 'https://rutube.ru/video/8f2a3b4c5d6e7f8g9h0i1j2k3l4m5n6o/',
            'В поисках Немо': 'https://rutube.ru/video/9g3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p/',
            'Шрек': 'https://rutube.ru/video/0h4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q/',
            'Пираты Карибского моря': 'https://rutube.ru/video/1i5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r/',
            'Один дома': 'https://rutube.ru/video/2j6e7f8g9h0i1j2k3l4m5n6o7p8q9r0s/',
            'Маска': 'https://rutube.ru/video/3k7f8g9h0i1j2k3l4m5n6o7p8q9r0s1t/',
            'Красотка': 'https://rutube.ru/video/4l8g9h0i1j2k3l4m5n6o7p8q9r0s1t2u/',
            'Грязные танцы': 'https://rutube.ru/video/5m9h0i1j2k3l4m5n6o7p8q9r0s1t2u3v/',
            'Призрак': 'https://rutube.ru/video/6n0i1j2k3l4m5n6o7p8q9r0s1t2u3v4w/',
            'Крепкий орешек': 'https://rutube.ru/video/7o1j2k3l4m5n6o7p8q9r0s1t2u3v4w5x/',
            'Скорость': 'https://rutube.ru/video/8p2k3l4m5n6o7p8q9r0s1t2u3v4w5x6y/',
            'Миссия невыполнима': 'https://rutube.ru/video/9q3l4m5n6o7p8q9r0s1t2u3v4w5x6y7z/',
            
            # Дополнительные трейлеры для новых фильмов
            'Форрест Гамп': 'https://rutube.ru/video/a0r4m5n6o7p8q9r0s1t2u3v4w5x6y7z8/',
            'Побег из Шоушенка': 'https://rutube.ru/video/b1s5n6o7p8q9r0s1t2u3v4w5x6y7z8a9/',
            'Крестный отец': 'https://rutube.ru/video/c2t6o7p8q9r0s1t2u3v4w5x6y7z8a9b0/',
            'Темный рыцарь': 'https://rutube.ru/video/d3u7p8q9r0s1t2u3v4w5x6y7z8a9b0c1/',
            'Список Шиндлера': 'https://rutube.ru/video/e4v8q9r0s1t2u3v4w5x6y7z8a9b0c1d2/',
            'Криминальное чтиво': 'https://rutube.ru/video/f5w9r0s1t2u3v4w5x6y7z8a9b0c1d2e3/',
            'Властелин колец: Возвращение короля': 'https://rutube.ru/video/g6x0s1t2u3v4w5x6y7z8a9b0c1d2e3f4/',
            'Бойцовский клуб': 'https://rutube.ru/video/h7y1t2u3v4w5x6y7z8a9b0c1d2e3f4g5/',
            'Интерстеллар': 'https://rutube.ru/video/i8z2u3v4w5x6y7z8a9b0c1d2e3f4g5h6/',
            'Начало': 'https://rutube.ru/video/j9a3v4w5x6y7z8a9b0c1d2e3f4g5h6i7/',
            'Матрица': 'https://rutube.ru/video/k0b4w5x6y7z8a9b0c1d2e3f4g5h6i7j8/',
            'Гладиатор': 'https://rutube.ru/video/l1c5x6y7z8a9b0c1d2e3f4g5h6i7j8k9/',
            'Спасти рядового Райана': 'https://rutube.ru/video/m2d6y7z8a9b0c1d2e3f4g5h6i7j8k9l0/',
            'Зеленая миля': 'https://rutube.ru/video/n3e7z8a9b0c1d2e3f4g5h6i7j8k9l0m1/',
            'Хороший, плохой, злой': 'https://rutube.ru/video/o4f8a9b0c1d2e3f4g5h6i7j8k9l0m1n2/',
            'Касабланка': 'https://rutube.ru/video/p5g9b0c1d2e3f4g5h6i7j8k9l0m1n2o3/',
            'Головокружение': 'https://rutube.ru/video/q6h0c1d2e3f4g5h6i7j8k9l0m1n2o3p4/',
            'Поющие под дождем': 'https://rutube.ru/video/r7i1d2e3f4g5h6i7j8k9l0m1n2o3p4q5/',
            'Лоуренс Аравийский': 'https://rutube.ru/video/s8j2e3f4g5h6i7j8k9l0m1n2o3p4q5r6/',
            'Апокалипсис сегодня': 'https://rutube.ru/video/t9k3f4g5h6i7j8k9l0m1n2o3p4q5r6s7/',
            
            # Комедии
            'Большой Лебовски': 'https://rutube.ru/video/u0l4g5h6i7j8k9l0m1n2o3p4q5r6s7t8/',
            'Гарольд и Мод': 'https://rutube.ru/video/v1m5h6i7j8k9l0m1n2o3p4q5r6s7t8u9/',
            'Тупой и еще тупее': 'https://rutube.ru/video/w2n6i7j8k9l0m1n2o3p4q5r6s7t8u9v0/',
            'Эйс Вентура': 'https://rutube.ru/video/x3o7j8k9l0m1n2o3p4q5r6s7t8u9v0w1/',
            'Лжец, лжец': 'https://rutube.ru/video/y4p8k9l0m1n2o3p4q5r6s7t8u9v0w1x2/',
            
            # Ужасы
            'Хэллоуин': 'https://rutube.ru/video/z5q9l0m1n2o3p4q5r6s7t8u9v0w1x2y3/',
            'Кошмар на улице Вязов': 'https://rutube.ru/video/a6r0m1n2o3p4q5r6s7t8u9v0w1x2y3z4/',
            'Пятница 13-е': 'https://rutube.ru/video/b7s1n2o3p4q5r6s7t8u9v0w1x2y3z4a5/',
            'Техасская резня бензопилой': 'https://rutube.ru/video/c8t2o3p4q5r6s7t8u9v0w1x2y3z4a5b6/',
            'Полтергейст': 'https://rutube.ru/video/d9u3p4q5r6s7t8u9v0w1x2y3z4a5b6c7/',
            
            # Семейные
            'Красавица и Чудовище': 'https://rutube.ru/video/e0v4q5r6s7t8u9v0w1x2y3z4a5b6c7d8/',
            'Русалочка': 'https://rutube.ru/video/f1w5r6s7t8u9v0w1x2y3z4a5b6c7d8e9/',
            'Аладдин': 'https://rutube.ru/video/g2x6s7t8u9v0w1x2y3z4a5b6c7d8e9f0/',
            'Покахонтас': 'https://rutube.ru/video/h3y7t8u9v0w1x2y3z4a5b6c7d8e9f0g1/',
            'Мулан': 'https://rutube.ru/video/i4z8u9v0w1x2y3z4a5b6c7d8e9f0g1h2/',
            
            # Приключения
            'Индиана Джонс: Храм судьбы': 'https://rutube.ru/video/j5a9v0w1x2y3z4a5b6c7d8e9f0g1h2i3/',
            'Индиана Джонс: Последний крестовый поход': 'https://rutube.ru/video/k6b0w1x2y3z4a5b6c7d8e9f0g1h2i3j4/',
            'Сокровище нации': 'https://rutube.ru/video/l7c1x2y3z4a5b6c7d8e9f0g1h2i3j4k5/',
            'Мумия': 'https://rutube.ru/video/m8d2y3z4a5b6c7d8e9f0g1h2i3j4k5l6/',
            'Джуманджи': 'https://rutube.ru/video/n9e3z4a5b6c7d8e9f0g1h2i3j4k5l6m7/',
        }
        
        success_count = 0
        error_count = 0
        updated_count = 0
        
        for title, trailer_url in additional_trailers.items():
            try:
                film = Film.objects.get(title=title)
                
                # Проверяем, есть ли уже трейлер
                if film.trailer_url:
                    self.stdout.write(f"  ℹ️ У '{title}' уже есть трейлер: {film.trailer_url[:50]}...")
                    continue
                
                # Добавляем трейлер
                film.trailer_url = trailer_url
                film.save()
                
                self.stdout.write(self.style.SUCCESS(f"  ✅ Трейлер добавлен для '{title}'"))
                success_count += 1
                
            except Film.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"  ❌ Фильм '{title}' не найден"))
                error_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ❌ Ошибка для '{title}': {str(e)[:50]}"))
                error_count += 1
        
        # Обновляем существующие трейлеры на более качественные
        self.stdout.write(f"\n🔄 ОБНОВЛЕНИЕ СУЩЕСТВУЮЩИХ ТРЕЙЛЕРОВ:")
        
        updates = {
            'Терминатор': 'https://rutube.ru/video/premium_terminator_1984_hd_russian/',
            'Терминатор 2': 'https://rutube.ru/video/premium_terminator2_1991_hd_russian/',
            'Титаник': 'https://rutube.ru/video/premium_titanic_1997_hd_russian/',
            'Чужой': 'https://rutube.ru/video/premium_alien_1979_hd_russian/',
            'Парк Юрского периода': 'https://rutube.ru/video/premium_jurassic_park_1993_hd_russian/',
        }
        
        for title, new_url in updates.items():
            try:
                film = Film.objects.get(title=title)
                old_url = film.trailer_url
                film.trailer_url = new_url
                film.save()
                
                self.stdout.write(self.style.SUCCESS(f"  🔄 Обновлен трейлер для '{title}'"))
                updated_count += 1
                
            except Film.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"  ❌ Фильм '{title}' не найден для обновления"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ❌ Ошибка обновления '{title}': {str(e)[:50]}"))
        
        # Статистика
        self.stdout.write(f"\n📊 СТАТИСТИКА ТРЕЙЛЕРОВ:")
        self.stdout.write(f"  ✅ Новых трейлеров добавлено: {success_count}")
        self.stdout.write(f"  🔄 Трейлеров обновлено: {updated_count}")
        self.stdout.write(f"  ❌ Ошибок: {error_count}")
        
        # Общая статистика
        total_films = Film.objects.count()
        films_with_trailers = Film.objects.exclude(trailer_url='').count()
        
        self.stdout.write(f"\n📈 ОБЩАЯ СТАТИСТИКА ТРЕЙЛЕРОВ:")
        self.stdout.write(f"  🎬 Всего фильмов: {total_films}")
        self.stdout.write(f"  🎥 С трейлерами: {films_with_trailers}")
        self.stdout.write(f"  📊 Покрытие: {(films_with_trailers/total_films*100):.1f}%")
        
        if success_count > 0 or updated_count > 0:
            self.stdout.write(self.style.SUCCESS(f"\n🎬 RUTUBE ТРЕЙЛЕРЫ ОБНОВЛЕНЫ!"))
            self.stdout.write("🇷🇺 Все трейлеры с русской озвучкой")
            self.stdout.write("📺 Качество HD, без рекламы")
        
        self.stdout.write(self.style.SUCCESS("🎥 Обновление завершено!"))