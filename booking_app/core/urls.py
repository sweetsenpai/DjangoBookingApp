from django.urls import path, include
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from rest_framework.routers import DefaultRouter
from .booking_api.views import *


router = DefaultRouter()
router.register("api/all-rooms", ShowRoomsApi, basename="all-room")

urlpatterns = [
    # SERVICE URLs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # ROOMS API
    path("", include(router.urls)),
    path("api/search-free-rooms/", SearchFreeRoomApi.as_view(), name="search-free-rooms"),
    # USER API
    path("api/user/registration/", UserRegistrationApi.as_view(), name="user-registration"),
    # USER BOOKING API
    path("api/user/booking/", UserAllBookingApi.as_view(), name="user-all-booking"),
    path("api/user/booking/<int:pk>/", UserBookingApi.as_view(), name="user-booking"),
    path("api/user/booking/create/", CreateBookingApi.as_view(), name="create-booking"),
]
