from django.urls import path

from .views import *

urlpatterns = [
    # ROOMS API
    path("all-rooms/", ShowRoomsApi.as_view(), name="all-rooms"),
    path("search-free-rooms/", SearchFreeRoomApi.as_view(), name="search-free-rooms"),
    # USER API
    path("user/registration/", UserRegistrationApi.as_view(), name="user-registration"),
    # USER BOOKING API
    path("user/booking/", UserAllBookingApi.as_view(), name="user-all-booking"),
    path("user/booking/<int:pk>/", UserBookingApi.as_view(), name="user-booking"),
    path("user/booking/create/", CreateBookingApi.as_view(), name="create-booking"),
]
