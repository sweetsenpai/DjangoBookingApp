from rest_framework.generics import ListAPIView

from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema

from booking_app_admin.models import Booking
from booking_app_api.v1.serializers import BookingSerializer


class ShowBookingApi(ListAPIView):
    queryset = Booking.objects.all().prefetch_related("room")
    serializer_class = BookingSerializer
