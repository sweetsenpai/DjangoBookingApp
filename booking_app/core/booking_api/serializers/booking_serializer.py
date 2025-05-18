from datetime import datetime
import logging

from rest_framework import serializers

from core.models import Booking

from .rooms_serializer import RoomSerializer
from .validators import validate_dates

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
        validate_dates(data["date_start"], data["date_end"])

        return data
