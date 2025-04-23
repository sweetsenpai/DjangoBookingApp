from rest_framework import serializers


class RoomSearchParamsSerializer(serializers.Serializer):
    date_start = serializers.DateField(required=True)
    date_end = serializers.DateField(required=True)
    capacity = serializers.IntegerField(required=False, min_value=0, default=0)
