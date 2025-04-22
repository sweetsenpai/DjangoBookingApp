from booking_app_api.v1.views import *
from django.urls import path

urlpatterns = [
    path("api/v1/all-rooms/", ShowRoomsApi.as_view(), name="all-rooms"),
    path("api/v1/all-booking/", ShowBookingApi.as_view(), name="all-booking"),
]
