from http.client import responses

from rest_framework import status
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.response import Response

from booking_app_admin.models import Booking
from booking_app_api.utils import IsOwnerOrSuperUser
from booking_app_api.v1.serializers import BookingSerializer


class UserBookingApi(RetrieveDestroyAPIView):
    queryset = Booking.objects.all().select_related("room")
    serializer_class = BookingSerializer
    permission_classes = [IsOwnerOrSuperUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        response_text = f"Бронь с id {instance.id} успешно удалена."
        self.perform_destroy(instance)
        return Response({"detail": response_text}, status=status.HTTP_200_OK)
