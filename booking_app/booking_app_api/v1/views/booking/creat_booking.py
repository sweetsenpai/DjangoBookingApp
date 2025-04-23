from rest_framework import status
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.response import Response

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)

from booking_app_admin.models import Booking
from booking_app_api.utils import IsOwnerOrSuperUser
from booking_app_api.v1.serializers import BookingSerializer