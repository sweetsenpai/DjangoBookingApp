from django.urls import path

from .views import *

urlpatterns = [
    path("all-rooms/", ShowRoomsApi.as_view(), name="all-rooms"),
    path("user/booking/", UserAllBookingApi.as_view(), name="user-all-booking"),
    path("user/booking/<int:pk>/", UserBookingApi.as_view(), name="user-booking"),
    path("user/booking/create/", CreateBookingApi.as_view(), name="create-booking"),
    path("search-free-rooms/", SearchFreeRoomApi.as_view(), name="search-free-rooms"),
]
