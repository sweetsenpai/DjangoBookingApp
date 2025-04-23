from django.urls import path

from booking_app_api.v1.views import *

urlpatterns = [
    path("api/v1/all-rooms/", ShowRoomsApi.as_view(), name="all-rooms"),
    path("api/v1/user/booking/", UserAllBookingApi.as_view(), name="user-all-booking"),
    path(
        "api/v1/user/booking/<int:pk>/", UserBookingApi.as_view(), name="user-booking"
    ),
]
