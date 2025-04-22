from rest_framework import serializers

from booking_app_admin.models import Room


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ["id", "name", "capacity", "price_per_day"]
