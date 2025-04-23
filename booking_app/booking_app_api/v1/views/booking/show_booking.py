from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema

from booking_app_admin.models import Booking
from booking_app_api.v1.serializers import BookingSerializer


class UserAllBookingApi(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all().prefetch_related("room")
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).prefetch_related("room")
