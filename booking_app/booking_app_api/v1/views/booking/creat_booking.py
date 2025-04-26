import logging

from booking_app_api.utils import BookingThrottle
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
        201: OpenApiResponse(
            response=BookingCreateSerializer,
            description="Успешный ответ",
            examples=[
                OpenApiExample(
                    name="Успешный ответ",
                    value={
                        "room": 1,
                        "date_start": "2025-07-01T00:00:00+03:00",
                        "date_end": "2025-07-03T00:00:00+03:00",
                    },
                    media_type="application/json",
                ),
            ],
        ),
        400: OpenApiResponse(
            response=BookingCreateSerializer,
            description="Ошибка валидации",
            examples=[
                OpenApiExample(
                    name="Указанная комната не существует",
                    value={
                        "room": [
                            'Недопустимый первичный ключ "0" - объект не существует.'
                        ]
                    },
                    media_type="application/json",
                ),
                OpenApiExample(
                    name="Не верный формат даты",
                    value={
                        "date_start": [
                            "Неправильный формат datetime. Используйте один из этих форматов:  YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
                        ]
                    },
                    media_type="application/json",
                ),
            ],
        ),
        409: OpenApiResponse(
            response=BookingCreateSerializer,
            description="Конфликт броней",
            examples=[
                OpenApiExample(
                    name="Комната уже забронированна",
                    value={"detail": "Комната уже забронирована на указанные даты."},
                    media_type="application/json",
                ),
            ],
        ),
        429: OpenApiResponse(
            response=BookingCreateSerializer,
            description="Too Many Requests",
            examples=[
                OpenApiExample(
                    name="Error: Too Many Requests",
                    value={
                        "detail": "Запрос был проигнорирован. Expected available in 86391 seconds."
                    },
                    media_type="application/json",
                ),
            ],
        ),
        503: OpenApiResponse(
            response=BookingCreateSerializer,
            description="Ошибка сервера",
            examples=[
                OpenApiExample(
                    name="Произошла непредвиденая ошибка во время бронирования",
                    value={
                        "detail": "Сервис временно не доступен.\nПожалйста, перезагрузите страницу и попробуйте ещё раз."
                    },
                    media_type="application/json",
                ),
            ],
        ),
    },
)
class CreateBookingApi(APIView):
    """
    API для создания новой брони.

    Этот API позволяет авторизованным пользователям создавать новые бронирования для комнат на заданные даты.
    Бронь создается с указанием даты начала, окончания и id номера. В случае ошибок, возвращаются соответствующие сообщения
    с кодами статуса.

    Валидация включает проверку существования комнаты, формата дат и пересечения броней.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [BookingThrottle]
    serializer_class = BookingCreateSerializer

    def post(self, request):
        """
        Метод для создания новой брони.

        Этот метод обрабатывает POST-запрос для создания новой брони.
        После успешной валидации данных, бронь сохраняется в базе данных.
        Возможные коды ответа:
        - 201: Успешное создание новой брони.
        - 400: Ошибка валидации данных.
        - 409: Конфликт. Комната уже забронирована для указанных дат.
        - 503: Непредвиденная ошибка сервиса.

        Параметры:
        - room (int): Идентификатор комнаты.
        - date_start (datetime): Начало брони.
        - date_end (datetime): Конец брони.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.validated_data["user"] = request.user
                serializer.save()
                logger.info(
                    f"Пользователь с id  {request.user.id} создал новое бронирование {serializer.data}"
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Обработка исключения от postgresql при попытке создания пересекающихся броней.
        except IntegrityError:
            return Response(
                {
                    "detail": "Комната уже забронирована. Попробуйте изменить даты бронирования или выберите другую комнату."
                },
                status=status.HTTP_409_CONFLICT,
            )
        except Exception as e:
            logger.error(
                "Во время создания нового бронирования произошла непредвиденная ошибка:\n"
                f"user: {request.user}\n"
                f"data: {request.data}\n"
                f"error: {str(e)}\n"
                f"error_type: {type(e)}"
            )
            return Response(
                {
                    "detail": "Сервис временно недоступен.Пожалуйста, перезагрузите страницу и попробуйте ещё раз."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
