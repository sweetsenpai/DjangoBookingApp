from .settings_dev import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "testdb",
        "PORT": "5432",
    }
}

# Отключить отправку email
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


# Дополнительные настройки для тестирования
CACHE_BACKEND = "django.core.cache.backends.locmem.LocMemCache"
DEBUG_TOOLBAR_PANELS = []
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,  # Отключение всех логеров
}
