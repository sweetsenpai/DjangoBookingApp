from booking_app_admin.models import Room
from rest_framework import serializers


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ["id", "name", "capacity", "price_per_day"]
