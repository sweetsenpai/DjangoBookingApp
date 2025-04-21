from booking_app_api.v1.views import ShowRooms
from django.urls import path

urlpatterns = [
    path("api/v1/all-rooms/", ShowRooms.as_view(), name="all-rooms"),
]
