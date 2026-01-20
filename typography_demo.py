from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Демонстрация новой красивой типографики'

    def handle(self, *args, **options):
        self.stdout.write("✨ TochkaFilms - Новая Типографика")
        self.stdout.write("=" * 50)
        
        self.stdout.write("\n🎨 НОВЫЕ ШРИФТЫ:")
        self.stdout.write("  📖 Inter - основной текст (современный, читаемый)")
        self.stdout.write("  🎭 Playfair Display - заголовки (элегантный, serif)")
        self.stdout.write("  🚀 Poppins - логотип и акценты (геометричный)")
        self.stdout.write("  💻 JetBrains Mono - код и техническая информация")
        
        self.stdout.write("\n🎪 СТИЛИ ЗАГОЛОВКОВ:")
        self.stdout.write("  🎬 cinematic-title - кинематографический стиль")
        self.stdout.write("  🌈 gradient-text-red - красный градиент")
        self.stdout.write("  🌟 gradient-text-gold - золотой градиент")
        self.stdout.write("  💙 gradient-text-blue - синий градиент")
        self.stdout.write("  ✨ text-glow - эффект свечения")
        self.stdout.write("  🎭 neon-text - неоновый эффект")
        
        self.stdout.write("\n📝 СТИЛИ ТЕКСТА:")
        self.stdout.write("  📚 readable-text - улучшенная читаемость")
        self.stdout.write("  🎨 elegant-text - элегантный курсив")
        self.stdout.write("  🔧 modern-text - современный минимализм")
        self.stdout.write("  💻 code-text - стиль кода")
        self.stdout.write("  📖 subtitle - стиль подзаголовков")
        self.stdout.write("  💬 quote - стиль цитат")
        
        self.stdout.write("\n🎯 УЛУЧШЕНИЯ:")
        self.stdout.write("  ⚡ Оптимизированная загрузка шрифтов")
        self.stdout.write("  📱 Адаптивные размеры (clamp)")
        self.stdout.write("  🎨 Сглаживание шрифтов")
        self.stdout.write("  ✨ Лигатуры и кернинг")
        self.stdout.write("  🌈 Градиентные эффекты")
        self.stdout.write("  💫 Анимированные градиенты")
        
        self.stdout.write("\n🎨 ЦВЕТОВАЯ СХЕМА ТЕКСТА:")
        self.stdout.write("  ⚪ #fff - основные заголовки")
        self.stdout.write("  🔘 #e0e0e0 - основной текст")
        self.stdout.write("  🔴 #e50914 - акцентный цвет")
        self.stdout.write("  🔸 #b0b0b0 - вторичный текст")
        self.stdout.write("  🔹 #d0d0d0 - цитаты")
        
        self.stdout.write("\n📐 ТИПОГРАФИЧЕСКИЕ ПРАВИЛА:")
        self.stdout.write("  📏 line-height: 1.7 - комфортное чтение")
        self.stdout.write("  📝 letter-spacing: оптимизированный")
        self.stdout.write("  🎯 font-weight: правильная иерархия")
        self.stdout.write("  📱 Responsive: clamp() для всех размеров")
        self.stdout.write("  ✨ text-rendering: optimizeLegibility")
        
        self.stdout.write("\n🎪 СПЕЦИАЛЬНЫЕ ЭФФЕКТЫ:")
        self.stdout.write("  🌊 Анимированные градиенты")
        self.stdout.write("  💫 Плавные переходы")
        self.stdout.write("  ✨ Тени и свечение")
        self.stdout.write("  🎨 Выделение текста")
        self.stdout.write("  🔮 3D эффекты")
        
        self.stdout.write("\n📱 АДАПТИВНОСТЬ:")
        self.stdout.write("  📱 Мобильные: оптимизированные размеры")
        self.stdout.write("  💻 Планшеты: средние размеры")
        self.stdout.write("  🖥️ Десктоп: полные размеры")
        self.stdout.write("  ⚡ Производительность: font-display: swap")
        
        self.stdout.write("\n🎭 ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:")
        self.stdout.write("  🎬 Главная страница: cinematic-title")
        self.stdout.write("  🔍 Поиск: gradient заголовки")
        self.stdout.write("  📚 Карточки: Poppins + Inter")
        self.stdout.write("  💬 Цитаты: Playfair Display italic")
        self.stdout.write("  🏷️ Бейджи: Inter uppercase")
        
        self.stdout.write(self.style.SUCCESS("\n🎉 Типографика обновлена!"))
        
        self.stdout.write("\n🌐 ТЕСТИРОВАНИЕ:")
        self.stdout.write("  1. Откройте: http://127.0.0.1:8000/")
        self.stdout.write("  2. Обратите внимание на новые шрифты")
        self.stdout.write("  3. Проверьте заголовки с градиентами")
        self.stdout.write("  4. Посмотрите на читаемость текста")
        self.stdout.write("  5. Протестируйте на разных устройствах")
        
        self.stdout.write("\n💡 ОСОБЕННОСТИ:")
        self.stdout.write("  🎨 Google Fonts для лучшего качества")
        self.stdout.write("  ⚡ Preconnect для быстрой загрузки")
        self.stdout.write("  📱 Clamp() для идеальной адаптивности")
        self.stdout.write("  ✨ Современные CSS свойства")
        self.stdout.write("  🎭 Кинематографический стиль")
        
        self.stdout.write("\n📁 ОБНОВЛЕННЫЕ ФАЙЛЫ:")
        self.stdout.write("  📄 films/templates/films/base.html - Google Fonts")
        self.stdout.write("  📄 static/css/style.css - новая типографика")
        self.stdout.write("  📄 films/templates/films/home.html - стили заголовков")
        self.stdout.write("  📄 films/templates/films/search.html - обновлен")
        
        self.stdout.write(self.style.SUCCESS("\n🚀 Сайт теперь имеет профессиональную типографику!"))