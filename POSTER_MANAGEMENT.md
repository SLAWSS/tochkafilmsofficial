# Управление постерами фильмов

## Доступные команды

### 1. Проверка фильмов без постеров
```bash
python manage.py find_missing_posters
```
Показывает все фильмы без постеров или с несуществующими файлами.

### 2. Добавление постеров всем фильмам без них
```bash
python manage.py add_all_posters
```
Автоматически создает красивые постеры для всех фильмов без них.

### 3. Скачивание постеров через API
```bash
python manage.py fetch_posters_api --film-id 123
python manage.py fetch_posters_api --search-term "Название фильма"
```
Загружает постеры через TMDB или OMDB API (требует API ключи).

### 4. Скачивание постеров по URL
```bash
python manage.py download_posters --film-id 123
python manage.py download_posters --all-missing
```
Скачивает постеры по заранее подготовленным URL.

### 5. Управление постерами
```bash
python manage.py manage_posters --check
python manage.py manage_posters --film-id 123 --poster-path /path/to/poster.jpg
```
Универсальная команда для управления постерами.

## Автоматическое создание постеров

Команда `add_all_posters` создает красивые постеры с:
- Градиентным фоном
- Названием фильма по центру
- Годом выпуска
- Декоративными элементами
- Разными цветовыми схемами

## Структура файлов

Постеры сохраняются в:
- `media/posters/` - основная папка
- Имена файлов: `название_фильма_poster.jpg`

## Примеры использования

### Добавить постеры всем новым фильмам:
```bash
python manage.py add_all_posters
```

### Проверить статус постеров:
```bash
python manage.py find_missing_posters
```

### Добавить постер конкретному фильму:
```bash
python manage.py manage_posters --film-id 123 --poster-path poster.jpg
```

## Требования

- Python 3.x
- Django
- Pillow (для создания изображений)
- requests (для скачивания из интернета)

## Установка зависимостей

```bash
pip install Pillow requests
```