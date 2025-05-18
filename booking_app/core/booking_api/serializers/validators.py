from datetime import datetime

from django.utils import timezone

from rest_framework.serializers import ValidationError


def validate_dates(date_start: datetime, date_end: datetime) -> None:
    """
    Валидирует времменой интервал
    :param date_start: дата заезда
    :param date_end: дата выезда
    :return: None
    """
    now = timezone.now()

    if date_start >= date_end:
        raise ValidationError("Дата заезда не может быть позже даты выезда.")

    if date_start < now:
        raise ValidationError("Дата заезда не может быть в прошлом.")

    if date_end < now:
        raise ValidationError("Дата выезда не может быть в прошлом.")
