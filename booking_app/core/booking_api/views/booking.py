from distutils.command.install import value

from django.db.utils import IntegrityError

from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)

from core.booking_api.serializers import BookingCreateSerializer, BookingSerializer
from core.models import Booking, Room
from core.utils.premissions import IsOwnerOrSuperUser

# Примеры данных
example_booking = {
    "id": 12,
    "room": {"id": 5, "name": "Люкс на двоих", "price_per_day": 3500, "capacity": 2},
    "date_start": "2025-06-01",
    "date_end": "2025-06-05",
}

example_create_request = {
    "room": 5,
    "date_start": "2025-06-01",
    "date_end": "2025-06-05",
}

example_conflict = {
    "detail": "Комната уже забронирована. Попробуйте изменить даты бронирования или выберите другую комнату."
}


@extend_schema_view(
    list=extend_schema(
        summary="Список бронирований текущего пользователя",
        description="Возвращает список всех бронирований, сделанных текущим пользователем.",
        responses={
            200: OpenApiResponse(
                response=BookingSerializer(many=True),
                description="Список бронирований",
                examples=[
                    OpenApiExample(
                        name="Пример ответа",
                        value=[example_booking],
                        media_type="application/json",
                    )
                ],
            ),
        },
    ),
    create=extend_schema(
        summary="Создание бронирования",
        description="""
            Создает новое бронирование для выбранной комнаты и указанного временного промежутка.
            
            Поля:
            - `room`: ID комнаты
            - `date_start`: дата заезда (формат YYYY-MM-DD)
            - `date_end`: дата выезда (формат YYYY-MM-DD)
            """,
        request=BookingCreateSerializer,
        responses={
            201: OpenApiResponse(
                response=BookingSerializer,
                description="Успешное создание бронирования",
                examples=[
                    OpenApiExample(
                        name="Успешный ответ",
                        value=example_booking,
                        media_type="application/json",
                    )
                ],
            ),
            409: OpenApiResponse(
                description="Конфликт бронирования",
                response=BookingSerializer,
                examples=[
                    OpenApiExample(
                        name="Конфликт бронирования",
                        value=example_conflict,
                        media_type="application/json",
                    )
                ],
            ),
        },
        examples=[
            OpenApiExample(
                name="Пример запроса",
                value=example_create_request,
                media_type="application/json",
            )
        ],
    ),
    destroy=extend_schema(
        summary="Удаление бронирования",
        description="Удаляет бронирование пользователя по его ID. Доступно только владельцу бронирования и суперпользователю.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=int,
                location=OpenApiParameter.PATH,
                description="`id` удаляемой брони",
            ),
        ],
        responses={
            204: OpenApiResponse(
                description="Бронирование успешно удалено",
            ),
            401: OpenApiResponse(
                description="Пользователь не авторизован.",
            ),
            404: OpenApiResponse(
                description="Запись с указанным `ID` не существует или не принадлежит пользователю.",
                response=serializers.Serializer,
                examples=[
                    OpenApiExample(
                        name="Не найдено",
                        value={"detail": "No Booking matches the given query."},
                        media_type="application/json",
                    )
                ],
            ),
        },
    ),
)
class BookingAPI(ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsOwnerOrSuperUser, IsAuthenticated]
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).prefetch_related("room")

    def get_serializer_class(self):
        if self.action == "create":
            return BookingCreateSerializer
        return BookingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {
                    "detail": "Комната уже забронирована. Попробуйте изменить даты бронирования или выберите другую комнату."
                },
                status=status.HTTP_409_CONFLICT,
            )
