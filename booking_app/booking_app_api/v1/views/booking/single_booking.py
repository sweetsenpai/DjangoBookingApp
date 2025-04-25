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


@extend_schema_view(
    get=extend_schema(
        summary="Получение информации о конкретной брони пользователя.",
        description="Получение детальной информации о конкретной брони пользователем-владельцем или суперпользователем.",
        parameters=[
            OpenApiParameter(
                name="id",
                description="id брони.",
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=BookingSerializer,
                description="Успешный ответ",
                examples=[
                    OpenApiExample(
                        name="Стандартный ответ",
                        value={
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
                        media_type="application/json",
                    ),
                ],
            ),
            401: OpenApiResponse(
                description="Пользователь не авторизован.",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Без авторизации",
                        value={"detail": "Учетные данные не были предоставлены."},
                        media_type="application/json",
                    )
                ],
            ),
            403: OpenApiResponse(
                description="Нет доступа к ресурсу.",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Чужая бронь",
                        value={
                            "detail": "У вас недостаточно прав для выполнения данного действия."
                        },
                        media_type="application/json",
                    )
                ],
            ),
        },
    ),
    delete=extend_schema(
        summary="Удаление конкретной брони пользователя.",
        parameters=[
            OpenApiParameter(
                name="id",
                description="id брони.",
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            )
        ],
        description="Удаление брони. Доступно только владельцу или суперпользователю.",
        responses={
            200: OpenApiResponse(
                response=BookingSerializer,
                description="Успешное удаление",
                examples=[
                    OpenApiExample(
                        name="Стандартный ответ",
                        value={"detail": "Бронь с id 1 успешно удалена."},
                        media_type="application/json",
                    ),
                ],
            ),
            401: OpenApiResponse(
                description="Пользователь не авторизован.",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Без авторизации",
                        value={"detail": "Учетные данные не были предоставлены."},
                        media_type="application/json",
                    )
                ],
            ),
            403: OpenApiResponse(
                description="Нет доступа к ресурсу.",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Чужая бронь",
                        value={
                            "detail": "У вас недостаточно прав для выполнения данного действия."
                        },
                        media_type="application/json",
                    )
                ],
            ),
        },
    ),
)
class UserBookingApi(RetrieveDestroyAPIView):
    queryset = Booking.objects.all().select_related("room")
    serializer_class = BookingSerializer
    permission_classes = [IsOwnerOrSuperUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        response_text = f"Бронь с id {instance.id} успешно удалена."
        self.perform_destroy(instance)
        return Response({"detail": response_text}, status=status.HTTP_200_OK)
