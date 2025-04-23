from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema

from booking_app_admin.models import Room
from booking_app_api.v1.serializers import RoomSerializer


class SearchFreeRoomApi(ListAPIView):
    queryset = Room.objects.all().prefetch_related("booking")
    serializer_class = RoomSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["price_per_day", "capacity"]
    ...
