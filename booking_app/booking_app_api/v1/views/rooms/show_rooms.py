from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema

from booking_app_admin.models import Room
from booking_app_api.v1.serializers import RoomSerializer


@extend_schema(
    summary="Список комнат с возможностью сортировки",
    description="Получить список всех комнат. Можно сортировать по `price_per_day` и `capacity`.",
    parameters=[
        OpenApiParameter(
            name="ordering",
            description="Поля сортировки: `price_per_day`, `capacity`.",
            required=False,
            type=str,
            location=OpenApiParameter.QUERY,
        )
    ],
    responses={200: RoomSerializer(many=True)},
    examples=[
        OpenApiExample(
            name="Ответ без параметра",
            value=[
                {
                    "id": 1,
                    "name": "Для двоих",
                    "price_per_day": "100.00",
                    "capacity": 2,
                },
                {
                    "id": 2,
                    "name": "Для одного",
                    "price_per_day": "50.00",
                    "capacity": 1,
                },
                {
                    "id": 3,
                    "name": "Для троих",
                    "price_per_day": "150.00",
                    "capacity": 3,
                },
            ],
            media_type="application/json",
        ),
        OpenApiExample(
            name="Ответ с сортировкой по цене",
            value=[
                {
                    "id": 2,
                    "name": "Для одного",
                    "price_per_day": "50.00",
                    "capacity": 1,
                },
                {
                    "id": 1,
                    "name": "Для двоих",
                    "price_per_day": "100.00",
                    "capacity": 2,
                },
                {
                    "id": 3,
                    "name": "Для троих",
                    "price_per_day": "150.00",
                    "capacity": 3,
                },
            ],
            media_type="application/json",
        ),
    ],
)
class ShowRoomsApi(ListAPIView):
    """
    API endpoint - возвращает список из всех комнат,
    с возможностью сортировки по полям price_per_day и capacity.

    Каждый элемент списка содержит id, name, price_per_day, capacity.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["price_per_day", "capacity"]
