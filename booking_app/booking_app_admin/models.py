import logging
from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import (DateTimeRangeField, RangeBoundary,
                                            RangeOperators)
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Func, Q


class Room(models.Model):
    name = models.CharField(
        max_length=100, help_text="Название/номер комнаты", unique=True, blank=False
    )
    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Стоимость комнаты за сутки",
    )
    capacity = models.IntegerField(
        help_text="Колличесвто человек на которое расчитана комната",
        blank=False,
        null=False,
        validators=[MinValueValidator(1)],
    )

    def __str__(self):
        return self.name


class TsTzRange(Func):
    function = "TSTZRANGE"
    outpput_field = DateTimeRangeField()


class Booking(models.Model):
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            ExclusionConstraint(
                name="exclude_overlapping_booking",
                expressions=[
                    (
                        TsTzRange("date_start", "date_end", RangeBoundary()),
                        RangeOperators.OVERLAPS,
                    ),
                    ("room", RangeOperators.EQUAL),
                ],
            )
        ]

    def __str__(self):
        return f"{self.user.username} – {self.room.name} – {self.date_start:%Y-%m-%d}"
