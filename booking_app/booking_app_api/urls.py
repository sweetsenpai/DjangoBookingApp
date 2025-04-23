# booking_app_api/urls.py (или основной urls.py проекта)
from django.urls import path, include

urlpatterns = [
    path("api/v1/", include("booking_app_api.v1.urls")),
]
