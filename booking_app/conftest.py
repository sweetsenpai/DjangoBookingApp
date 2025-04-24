import pytest
from django.apps import apps
from django.conf import settings
from django.db import connection


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "testdb",
        "PORT": "5432",
        "ATOMIC_REQUESTS": True,
    }



