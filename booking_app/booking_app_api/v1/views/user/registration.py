import logging

from django.contrib.auth.models import User
from django.db import transaction

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework_simplejwt.tokens import RefreshToken

from booking_app_api.utils import UserRegistrationThrottle
from booking_app_api.v1.serializers import RegistrationSerializer

logger = logging.getLogger(__name__)


@extend_schema(
    summary="Регистрация",
    description="Создание нового пользователя. В случае успеха возвращает access_token.",
    request=RegistrationSerializer,
    responses={
        201: OpenApiResponse(
            response=RegistrationSerializer,
            description="Успешный ответ",
            examples=[
                OpenApiExample(
                    name="Успешный ответ",
                    value={"access_token": "MTV9.J1gJ9ZNlo..."},
                    media_type="application/json",
                ),
            ],
        ),
        400: OpenApiResponse(
            response=RegistrationSerializer,
            description="Ошибка валидации",
            examples=[
                OpenApiExample(
                    name="Не уникальное имя пользователя",
                    value={
                        "username": ["Пользователь с таким именем уже существует."],
                    },
                    media_type="application/json",
                ),
                OpenApiExample(
                    name="Не уникальный email",
                    value={"email": ["Значения поля должны быть уникальны."]},
                    media_type="application/json",
                ),
                OpenApiExample(
                    name="Слабый пароль",
                    value={
                        "password": [
                            "This password is too short. It must contain at least 8 characters.",
                            "Введённый пароль слишком широко распространён.",
                            "Введённый пароль состоит только из цифр.",
                        ]
                    },
                    media_type="application/json",
                ),
            ],
        ),
        429: OpenApiResponse(
            response=RegistrationSerializer,
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
        500: OpenApiResponse(
            response=RegistrationSerializer,
            description="Server Error",
            examples=[
                OpenApiExample(
                    name="Server Error",
                    value={
                        "detail": "Произошла непредвиденная ошибка. Попробуйте позднее."
                    },
                    media_type="application/json",
                ),
            ],
        ),
    },
)
class UserRegistrationApi(generics.CreateAPIView):
    """
    API эндпоинт для регистрации нового пользователя.

    Данный эндпоинт создает нового пользователя с предоставленными данными (username, password, password2, email),
    валидирует их и возвращает access_token при успешной регистрации.


    Примечание:
    - Этот эндпоинт доступен без авторизации.
    - Данные в поле password должны удовлетворять требованиям безопасности (минимальная длина, сложность).
    """

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer
    throttle_classes = [UserRegistrationThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            with transaction.atomic():
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                response_data = {
                    "access_token": str(refresh.access_token),
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
        except ValidationError:
            raise

        except Exception as e:
            logger.error(
                "Вовремя регистрации нового пользователя проищошла непредвиденая ошибка.\n"
                f"data: {request.data}\n"
                f"error: {str(e)}"
            )
            return Response(
                {"detail": "Произошла непредвиденная ошибка. Попробуйте позднее."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
