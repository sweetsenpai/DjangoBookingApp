import logging

from core.filters import get_free_rooms
from core.models import Booking
from rest_framework import serializers

from ..Room.rooms_serializer import RoomSerializer

logger = logging.getLogger(__name__)


class BookingSerializer(serializers.ModelSerializer):
    room = RoomSerializer()

    class Meta:
        model = Booking
        fields = ["id", "date_start", "date_end", "room"]


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["room", "date_start", "date_end"]

    def validate(self, data):
        logger.debug(
            "Дата начала бронирования: %s, Тип данных: %s",
            data["date_start"],
            type(data["date_start"]),
        )
        if data["date_start"] >= data["date_end"]:
            raise serializers.ValidationError(
                "Дата начала бронирования не может быть позже даты конца."
            )

        # Проверка доступности комнаты на этот период
        logger.debug(
            "Проверка свободна ли комната:\n"
            f"комната: {data['room']}\n"
            f"свободные комнаты:{get_free_rooms(data['date_start'], data['date_end'])}"
        )

        return data
