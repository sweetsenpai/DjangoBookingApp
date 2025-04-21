from booking_app_admin.models import Room
from booking_app_api.v1.serializers import RoomSerializer
from rest_framework.generics import ListAPIView


class ShowRooms(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
