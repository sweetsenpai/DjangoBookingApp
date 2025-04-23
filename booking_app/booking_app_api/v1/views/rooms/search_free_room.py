from django.db.models import Q

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)

from booking_app_admin.models import Booking, Room
from booking_app_api.v1.serializers import RoomSearchParamsSerializer, RoomSerializer


@extend_schema(
    summary="Поиск по доступным комнатам",
    description="Поиск по доступным комнатам в указанный временной промежуток с возхможностью так же указать вместительность комнаты.",
    parameters=[
        OpenApiParameter(
            "date_start",
            str,
            required=True,
            description="Начальная дата бронирования (YYYY-MM-DD)",
        ),
        OpenApiParameter(
            "date_end",
            str,
            required=True,
            description="Конечная дата бронирования (YYYY-MM-DD)",
        ),
        OpenApiParameter(
            "capacity",
            str,
            required=False,
            description="Максимальное число жильцов",
        ),
    ],
    responses=RoomSerializer(many=True),
    examples=[
        OpenApiExample(
            name="Стандартный ответ",
            value=[
                {
                    "id": 1,
                    "name": "Для двоих",
                    "price_per_day": "100.00",
                    "capacity": 2,
                }
            ],
        ),
        OpenApiExample(
            name="Ответ когда не удалось найти комнату по заданым параметрам.", value=[]
        ),
    ],
)
class SearchFreeRoomApi(APIView):

    def get(self, request):
        serializer = RoomSearchParamsSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated = serializer.validated_data
        date_start = validated["date_start"]
        date_end = validated["date_end"]
        capacity = validated["capacity"]

        busy_rooms = Booking.objects.filter(
            Q(date_start__lt=date_end) & Q(date_end__gt=date_start)
        ).values_list("room_id", flat=True)

        free_rooms = Room.objects.exclude(id__in=busy_rooms).filter(
            capacity__gte=capacity
        )
        serializer = RoomSerializer(free_rooms, many=True)

        return Response(serializer.data)
