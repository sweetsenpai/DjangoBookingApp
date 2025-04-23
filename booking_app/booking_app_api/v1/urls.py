from django.urls import path

from .views import *

urlpatterns = [
    path("all-rooms/", ShowRoomsApi.as_view(), name="all-rooms"),
    path("user/booking/", UserAllBookingApi.as_view(), name="user-all-booking"),
    path(
        "user/booking/<int:pk>/", UserBookingApi.as_view(), name="user-booking"
    ),
    path("free-rooms/", SearchFreeRoomApi.as_view(), name="free-rooms"),
]
