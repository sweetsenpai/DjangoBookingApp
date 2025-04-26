from datetime import datetime, time

from booking_app_admin.models import Booking, Room
from django.db.models import Q, QuerySet
from django.utils.timezone import get_current_timezone, make_aware


def get_free_rooms(date_start: datetime, date_end: datetime) -> QuerySet:
    """
    Поиск свободных комнат в заданный временной промежуток.

    :param date_start: дата заезда
    :param date_end: дата выезда
    :return: возвращает QuerySet с доступными комнатами по заданым параметрам
    """

    busy_rooms = Booking.objects.filter(
        Q(date_start__lt=date_end) & Q(date_end__gt=date_start)
    ).values_list("room_id", flat=True)
    free_rooms = Room.objects.exclude(id__in=busy_rooms)
    return free_rooms
