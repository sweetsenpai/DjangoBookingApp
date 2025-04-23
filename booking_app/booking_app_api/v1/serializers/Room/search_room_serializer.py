from datetime import date

from rest_framework import serializers


class RoomSearchParamsSerializer(serializers.Serializer):
    date_start = serializers.DateField(required=True)
    date_end = serializers.DateField(required=True)
    capacity = serializers.IntegerField(required=False, min_value=0, default=0)

    def validate(self, data):
        if data["date_start"] > data["date_end"]:
            raise serializers.ValidationError(
                "Дата заезда не может быть позже даты выезда."
            )
        if data["date_end"] < date.today():
            raise serializers.ValidationError("Дата выезда не может быть в прошлом.")
        return data
