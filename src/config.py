import os

# Корневая папка проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Базовая папка с ресурсами
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# Путь к БД
DB_PATH = os.path.join(BASE_DIR, 'data', 'echo_database.db')

# --- УДОБНЫЙ ДОСТУП К КАРТИНКАМ ---
class Assets:
    # Логотипы
    LOGO_MONOCOLOR = os.path.join(ASSETS_DIR, 'logo', 'logo_monocolor.png')
    LOGO_HOVER = os.path.join(ASSETS_DIR, 'logo', 'logo_hover.png')
    LOGO_PRESSED = os.path.join(ASSETS_DIR, 'logo', 'logo_pressed.png')

    # Иконки интерфейса
    ICON_HEART = os.path.join(ASSETS_DIR, 'icons', 'heart.png')
    ICON_HEART_HOVER = os.path.join(ASSETS_DIR, 'icons', 'heart2.png')
    ICON_HEART_WHITE = os.path.join(ASSETS_DIR, 'icons', 'heart_white.png')
    ICON_BOOKMARK = os.path.join(ASSETS_DIR, 'icons', 'bookmark.png')
    ICON_BOOKMARK_HOVER = os.path.join(ASSETS_DIR, 'icons', 'bookmark2.png')
    ICON_BOOKMARK_WHITE = os.path.join(ASSETS_DIR, 'icons', 'bookmark_white.png')
    ICON_SEARCH = os.path.join(ASSETS_DIR, 'icons', 'Search.png')
    ICON_PROFILE = os.path.join(ASSETS_DIR, 'icons', 'profile.png')
    ICON_EYE_OPENED = os.path.join(ASSETS_DIR, 'icons', 'eyeOpened.png')
    ICON_EYE_CLOSED = os.path.join(ASSETS_DIR, 'icons', 'eyeClosed.png')
    ICON_SETTINGS = os.path.join(ASSETS_DIR, 'icons', 'settings.png')
    ICON_CROSS = os.path.join(ASSETS_DIR, 'icons', 'cross.png')
    ICON_ARROW_DOWN = os.path.join(ASSETS_DIR, 'icons', 'arrow_down.png')

    # Иконки категорий
    CAT_POLITICS = os.path.join(ASSETS_DIR, 'icons', 'categories', 'earth.jpg')
    CAT_ECONOMY = os.path.join(ASSETS_DIR, 'icons', 'categories', 'coin.jpg')
    CAT_CULTURE = os.path.join(ASSETS_DIR, 'icons', 'categories', 'masks.jpg')
    CAT_SPORT = os.path.join(ASSETS_DIR, 'icons', 'categories', 'cup.jpg')
    CAT_SCIENCE = os.path.join(ASSETS_DIR, 'icons', 'categories', 'science.jpg')
    CAT_HEALTH = os.path.join(ASSETS_DIR, 'icons', 'categories', 'health.jpg')
    CAT_GAMES = os.path.join(ASSETS_DIR, 'icons', 'categories', 'gamepad.jpg')
    CAT_HOT = os.path.join(ASSETS_DIR, 'icons', 'categories', 'hot.jpg')
    CAT_RECENT = os.path.join(ASSETS_DIR, 'icons', 'categories', 'recent.jpg')
    CAT_UNIVERSITY = os.path.join(ASSETS_DIR, 'icons', 'categories', 'university.jpg')

    # Иконки издательств
    PUB_RIA = os.path.join(ASSETS_DIR, 'icons', 'publish', 'ria.jpg')
    PUB_AIF = os.path.join(ASSETS_DIR, 'icons', 'publish', 'aif.jpg')
    PUB_TASS = os.path.join(ASSETS_DIR, 'icons', 'publish', 'tass.jpg')

    # Аватарки (генерируем пути для всех 16 штук)
    AVATARS = [os.path.join(ASSETS_DIR, 'avatars', f'avatar_{i}.png') for i in range(1, 17)]