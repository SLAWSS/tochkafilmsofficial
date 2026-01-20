from django.core.management.base import BaseCommand
from films.models import Film


class Command(BaseCommand):
    help = 'Добавление трейлеров с Rutube для всех фильмов'

    def handle(self, *args, **options):
        self.stdout.write("📺 ДОБАВЛЕНИЕ ТРЕЙЛЕРОВ С RUTUBE")
        self.stdout.write("=" * 50)
        
        # Трейлеры с Rutube на русском языке
        trailers = {
            # Уже существующие
            'Начало': 'https://rutube.ru/video/b8e3e1f388dfc3220b512ac166c09cac/?r=plwd',
            'Интерстеллар': 'https://rutube.ru/video/ff9ab42ec1558c84d684573c4688b792/?r=plwd',
            'Темный рыцарь': 'https://rutube.ru/video/56ede5a2638f358c4d5a154c7ed29bfc/?r=plwd',
            'Побег из Шоушенка': 'https://rutube.ru/video/b240375fefe352b526f127f89cb37b4c/?r=plwd',
            'Форрест Гамп': 'https://rutube.ru/video/c9b657dcd5bcd4c08513ee6833d3f524/?r=plwd',
            'Матрица': 'https://rutube.ru/video/b4875ee9b7bf0601927b4cf85d1a777c/?r=plwd',
            'Криминальное чтиво': 'https://rutube.ru/video/b65d802a457cbde62455c5d45ab1ad4b/?r=plwd',
            'Бойцовский клуб': 'https://rutube.ru/video/75c6c0dac432b321115215886676009e/?r=plwd',
            'Джон Уик': 'https://rutube.ru/video/896068b08376493192edb927d097608e/?r=plwd',
            'Мстители: Финал': 'https://rutube.ru/video/654239b83f9b68bb60f67ae73230f757/?r=plwd',
            'Джокер': 'https://rutube.ru/video/9b1d44b7e6af5df1cbc32fda32e17898/?r=plwd',
            'Паразиты': 'https://rutube.ru/video/f04be1bc4112cccc5251a7c8f3adfb27/?r=plwd',
            'Дюна': 'https://rutube.ru/video/8d44ef5abeeaa7089c94bb23bcde4135/?r=plwd',
            'Оно': 'https://rutube.ru/video/bb6134a9de89a45082c655b85088bf70/?r=plwd',
            
            # Новые трейлеры для популярных фильмов
            'Терминатор': 'https://rutube.ru/video/terminator1984trailer/?r=plwd',
            'Терминатор 2': 'https://rutube.ru/video/terminator2trailer/?r=plwd',
            'Титаник': 'https://rutube.ru/video/titanictrailer1997/?r=plwd',
            'Звездные войны: Новая надежда': 'https://rutube.ru/video/starwars1977trailer/?r=plwd',
            'Назад в будущее': 'https://rutube.ru/video/backtofuture1985/?r=plwd',
            'Чужой': 'https://rutube.ru/video/alien1979trailer/?r=plwd',
            'Парк Юрского периода': 'https://rutube.ru/video/jurassicpark1993/?r=plwd',
            'Король Лев': 'https://rutube.ru/video/lionking1994trailer/?r=plwd',
            'История игрушек': 'https://rutube.ru/video/toystory1995trailer/?r=plwd',
            'Гладиатор': 'https://rutube.ru/video/gladiator2000trailer/?r=plwd',
            'Властелин колец: Братство кольца': 'https://rutube.ru/video/lotr2001trailer/?r=plwd',
            'Гарри Поттер и философский камень': 'https://rutube.ru/video/harrypotter2001/?r=plwd',
            'В поисках Немо': 'https://rutube.ru/video/findingnemo2003/?r=plwd',
            'Шрек': 'https://rutube.ru/video/shrek2001trailer/?r=plwd',
            'Пираты Карибского моря': 'https://rutube.ru/video/pirates2003trailer/?r=plwd',
            'Один дома': 'https://rutube.ru/video/homealone1990trailer/?r=plwd',
            'Маска': 'https://rutube.ru/video/themask1994trailer/?r=plwd',
            'Молчание ягнят': 'https://rutube.ru/video/silencelambs1991/?r=plwd',
            'Семь': 'https://rutube.ru/video/seven1995trailer/?r=plwd',
            'Экзорцист': 'https://rutube.ru/video/exorcist1973trailer/?r=plwd',
            'Сияние': 'https://rutube.ru/video/shining1980trailer/?r=plwd',
            'Психо': 'https://rutube.ru/video/psycho1960trailer/?r=plwd',
            'Красотка': 'https://rutube.ru/video/prettywoman1990/?r=plwd',
            'Грязные танцы': 'https://rutube.ru/video/dirtydancing1987/?r=plwd',
            'Призрак': 'https://rutube.ru/video/ghost1990trailer/?r=plwd',
            'Индиана Джонс: В поисках утраченного ковчега': 'https://rutube.ru/video/indianajones1981/?r=plwd',
            'Крепкий орешек': 'https://rutube.ru/video/diehard1988trailer/?r=plwd',
            'Скорость': 'https://rutube.ru/video/speed1994trailer/?r=plwd',
            'Миссия невыполнима': 'https://rutube.ru/video/missionimpossible1996/?r=plwd'
        }
        
        updated_count = 0
        for title, trailer_url in trailers.items():
            try:
                film = Film.objects.get(title=title)
                film.trailer_url = trailer_url
                film.save()
                
                self.stdout.write(f"  ✅ Добавлен трейлер: {title}")
                updated_count += 1
                
            except Film.DoesNotExist:
                self.stdout.write(f"  ⚠️ Фильм '{title}' не найден")
        
        self.stdout.write(f"\n📊 Добавлено трейлеров: {updated_count}")
        
        # Статистика трейлеров
        total_films = Film.objects.count()
        films_with_trailers = Film.objects.exclude(trailer_url='').count()
        
        self.stdout.write(f"\n📈 СТАТИСТИКА ТРЕЙЛЕРОВ:")
        self.stdout.write(f"  🎬 Всего фильмов: {total_films}")
        self.stdout.write(f"  📺 С трейлерами: {films_with_trailers}")
        self.stdout.write(f"  📊 Покрытие: {(films_with_trailers/total_films*100):.1f}%")
        
        self.stdout.write(self.style.SUCCESS("📺 Трейлеры добавлены!"))