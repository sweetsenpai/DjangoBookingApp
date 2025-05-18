from datetime import datetime, time

from django.db.models import Q, QuerySet
from django.utils import timezone

from rest_framework.serializers import ValidationError

from django_filters import rest_framework as filters

from core.booking_api.serializers.validators import validate_dates
from core.models import Booking, Room


class RoomFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price_per_day", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price_per_day", lookup_expr="lte")
    capacity = filters.NumberFilter(field_name="capacity", lookup_expr="gte")

    date_start = filters.DateFilter(method="filter_by_availability")
    date_end = filters.DateFilter(method="filter_by_availability")

    class Meta:
        model = Room
        fields = ["min_price", "max_price", "capacity", "date_start", "date_end"]

    def get_free_rooms(self, date_start: datetime, date_end: datetime) -> QuerySet:
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

    def filter_by_availability(self, queryset, name, value):
        date_start = self.form.cleaned_data.get("date_start")
        date_end = self.form.cleaned_data.get("date_end")

        if not date_start or not date_end:
            return queryset

        date_start_dt = timezone.make_aware(datetime.combine(date_start, time.min))
        date_end_dt = timezone.make_aware(datetime.combine(date_end, time.min))

        validate_dates(date_start_dt, date_end_dt)

        free_rooms = self.get_free_rooms(date_start_dt, date_end_dt)
        return queryset.filter(id__in=free_rooms.values_list("id", flat=True))
