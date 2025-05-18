from rest_framework import serializers

from core.models import Room


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ["id", "name", "capacity", "price_per_day"]
