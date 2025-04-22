from booking_app_admin.models import Booking
from booking_app_api.v1.serializers import BookingSerializer
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   extend_schema)
from rest_framework.generics import ListAPIView


class ShowBookingApi(ListAPIView):
    queryset = Booking.objects.all().prefetch_related("room")
    serializer_class = BookingSerializer
