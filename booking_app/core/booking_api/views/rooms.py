from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
)

from core.booking_api.serializers import RoomSerializer
from core.filters.rooms_filters import RoomFilter
from core.models import Room

example_response_simple = [
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
]

# Пример с сортировкой по возрастанию цены
example_response_ordered = [
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
]

# Пример с фильтром capacity=2
example_response_filtered = [
    {
        "id": 1,
        "name": "Для двоих",
        "price_per_day": "100.00",
        "capacity": 2,
    }
]


@extend_schema(
    summary="Список комнат с возможностью сортировки и фильтрации",
    description="Получить список всех комнат. Можно фильтровать по цене, вместимости и доступности в указанный временной промежуток, а также сортировать по полям `price_per_day`, `capacity`.",
    parameters=[
        OpenApiParameter(
            name="date_start",
            type=OpenApiTypes.DATETIME,
            location=OpenApiParameter.QUERY,
            description="Дата заезда (формат YYYY-MM-DD). Используется только вместе с `date_end`.",
        ),
        OpenApiParameter(
            name="date_end",
            type=OpenApiTypes.DATETIME,
            location=OpenApiParameter.QUERY,
            description="Дата выезда (формат YYYY-MM-DD). Используется только вместе с `date_start`.",
        ),
        OpenApiParameter(
            name="min_price",
            type=float,
            location=OpenApiParameter.QUERY,
            description="Минимальная цена за день (price_per_day ≥ X)",
        ),
        OpenApiParameter(
            name="max_price",
            type=float,
            location=OpenApiParameter.QUERY,
            description="Максимальная цена за день (price_per_day ≤ X)",
        ),
        OpenApiParameter(
            name="capacity",
            type=int,
            location=OpenApiParameter.QUERY,
            description="Минимальная вместимость комнаты (capacity ≥ X)",
        ),
        OpenApiParameter(
            name="ordering",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Поля для сортировки через запятую. `price_per_day, -price_per_day` и `capacity, -capacity`",
        ),
    ],
    responses={200: RoomSerializer(many=True)},
    examples=[
        OpenApiExample(
            name="Без параметров",
            value=example_response_simple,
            media_type="application/json",
        ),
        OpenApiExample(
            name="С сортировкой по цене",
            value=example_response_ordered,
            media_type="application/json",
        ),
        OpenApiExample(
            name="С фильтром: capacity=2",
            value=example_response_filtered,
            media_type="application/json",
        ),
    ],
)
class RoomsApi(ReadOnlyModelViewSet):
    """
    API endpoint - возвращает список из всех комнат,
    с возможностью сортировки и фильтрации по полям price_per_day и capacity, а так же поиском свободных комнат.

    Каждый элемент списка содержит id, name, price_per_day, capacity.
    """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RoomFilter
    ordering_fields = ["price_per_day", "capacity"]
    ordering = ["price_per_day"]

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method 'retrieve' not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
