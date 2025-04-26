from .settings_dev import *

DEBUG = True

INSTALLED_APPS.remove("debug_toolbar")

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
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,  # Отключение всех логеров
}
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_test')
STATICFILES_DIRS = []