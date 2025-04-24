import logging

from booking_app_api.v1.serializers import BookingCreateSerializer
from django.db import transaction
from django.db.utils import IntegrityError
from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   extend_schema)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


@extend_schema(
    summary="Создание новой брони",
    description="Создаёт новую бронь для комнаты на заданные даты. Требуется авторизация.",
    request=BookingCreateSerializer,
    responses={
        201: BookingCreateSerializer,
        400: OpenApiResponse(
            description="Ошибка валидации",
            examples=[
                OpenApiExample(
                    name="Ошибка валидации",
                    value={"detail": "Комната уже забронирована на указанные даты."},
                ),
            ],
        ),
    },
    examples=[
        OpenApiExample(
            name="Пример запроса",
            value={"room": 1, "date_start": "2025-05-01", "date_end": "2025-05-03"},
            request_only=True,
        ),
        OpenApiExample(
            name="Пример успешного ответа",
            value={
                "id": 123,
                "room": 1,
                "user": 5,
                "date_start": "2025-05-01",
                "date_end": "2025-05-03",
            },
            response_only=True,
        ),
    ],
)
class CreateBookingApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.validated_data["user"] = request.user
                serializer.save()
                logger.info(
                    f"Польщователь с id  {request.user.id} создал новое бронирование {serializer.data}"
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {
                        "detail": "Комната уже забронирована. Попробуйте изменить даты бронирования или выбирете другую комнату."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                logger.error(
                    "Во время создания нового бронирования произошла не предвиденая ошибка:\n"
                    f"user: {request.user}\n"
                    f"data: {request.data}\n"
                    f"error: {str(e)}\n"
                    f"error_type: {type(e)}"
                )
                return Response(
                    {
                        "detail": "Сервис временно не доступен.\nПожалйста, перезагрузите страницу и попробуйте ещё раз."
                    },
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
