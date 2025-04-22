from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from booking_app_admin.models import Booking, Room


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.room = Room.objects.create(name="103", price_per_day=150.0, capacity=3)

    def test_create_booking(self):
        start = timezone.now()
        end = start + timezone.timedelta(days=2)
        booking = Booking.objects.create(
            room=self.room, user=self.user, date_start=start, date_end=end
        )
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.date_start, start)
        self.assertEqual(booking.date_end, end)
