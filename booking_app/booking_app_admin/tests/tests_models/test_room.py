from django.core.exceptions import ValidationError
from django.test import TestCase

import pytest

from booking_app_admin.models import Room


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class RoomModelTest(TestCase):
    def test_create_room(self):
        room = Room.objects.create(name="101", price_per_day=100.0, capacity=2)
        self.assertEqual(room.name, "101")
        self.assertEqual(room.price_per_day, 100.0)
        self.assertEqual(room.capacity, 2)

    def test_room_capacity_cannot_be_less_than_one(self):
        with self.assertRaises(ValidationError):
            room = Room(name="102", price_per_day=100.0, capacity=0)
            room.full_clean()
