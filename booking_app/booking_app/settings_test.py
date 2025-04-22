from .settings_dev import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",  # База данных в памяти для быстрого тестирования
    }
}

# Отключить отправку email
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Включить дебаг, если нужно
DEBUG = True

# Дополнительные настройки для тестирования
CACHE_BACKEND = "django.core.cache.backends.locmem.LocMemCache"
DEBUG_TOOLBAR_PANELS = []
