from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework_simplejwt.authentication import JWTAuthentication

from booking_app_admin.models import Booking
from booking_app_api.v1.serializers import BookingSerializer


@extend_schema(
    summary="Список всех броней текущего пользователя",
    description="Список всех броней текущего пользователя, с детальной информацией о забронированных комнатах.",
    responses={
        200: OpenApiResponse(
            response=BookingSerializer(many=True),
            description="Успешный ответ со списком броней",
            examples=[
                OpenApiExample(
                    name="Стандартный ответ",
                    value=[
                        {
                            "id": 1,
                            "date_start": "2025-04-01T00:00:00+03:00",
                            "date_end": "2025-04-06T00:00:00+03:00",
                            "room": {
                                "id": 1,
                                "name": "Одиночка",
                                "capacity": 1,
                                "price_per_day": "123.00",
                            },
                        },
                        {
                            "id": 2,
                            "date_start": "2025-04-11T00:00:00+03:00",
                            "date_end": "2025-04-16T00:00:00+03:00",
                            "room": {
                                "id": 2,
                                "name": "Для двоих",
                                "capacity": 2,
                                "price_per_day": "300.00",
                            },
                        },
                    ],
                    media_type="application/json",
                ),
            ],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Неавторизованный пользователь",
            examples=[
                OpenApiExample(
                    name="Ответ для не зарегистрированного пользователя",
                    value={"detail": "Учетные данные не были предоставлены."},
                    media_type="application/json",
                )
            ],
        ),
    },
)
class UserAllBookingApi(ListAPIView):
    """
    API endpoint для получения данных о всех бронированиях пользователя.

    Endpoint доступен только для зарегистрированных пользователей.

    Этот endpoint возвращает список объектов бронирования и связанную с ним комнату,
    по его id.

    Объект бронирования содержит в себе поля id, date_start, date_end, room(id, name, capacity, price_per_day).
    """
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all().prefetch_related("room")
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).prefetch_related("room")
