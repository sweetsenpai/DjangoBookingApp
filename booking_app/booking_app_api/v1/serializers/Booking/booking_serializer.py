from booking_app_admin.models import Booking
from rest_framework import serializers
from ..Room.rooms_serializer import RoomSerializer


class BookingSerializer(serializers.ModelSerializer):
    room = RoomSerializer()

    class Meta:
        model = Booking
        fields = ["id", "date_start", "date_end", "room"]
