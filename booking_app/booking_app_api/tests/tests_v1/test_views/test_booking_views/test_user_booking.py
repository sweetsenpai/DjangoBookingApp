from datetime import datetime
from decimal import Decimal

import pytest
from booking_app_admin.models import Booking, Room
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class UserBookingApiTest(APITestCase):
    def setUp(self):
        self.User = get_user_model()

        self.room1 = Room.objects.create(
            name="Для двоих", price_per_day=Decimal("100.00"), capacity=2
        )
        self.room2 = Room.objects.create(
            name="Для одного", price_per_day=Decimal("50.00"), capacity=1
        )

        self.superuser = self.User.objects.create_superuser(
            username="admin", password="admin"
        )
        self.user = self.User.objects.create_user(username="user", password="54321")

        self.start1 = timezone.make_aware(datetime(2021, 1, 1))
        self.end1 = timezone.make_aware(datetime(2021, 1, 2))

        self.start2 = timezone.make_aware(datetime(2021, 1, 3))
        self.end2 = timezone.make_aware(datetime(2021, 1, 4))

        self.booking1 = Booking.objects.create(
            room=self.room1,
            user=self.superuser,
            date_start=self.start1,
            date_end=self.end1,
        )
        self.booking2 = Booking.objects.create(
            room=self.room2, user=self.user, date_start=self.start2, date_end=self.end2
        )

    def test_get_user_rooms(self):
        self.client.login(username="user", password="54321")
        url = reverse("user-all-booking")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data[0]

        self.assertEqual(data["id"], self.booking2.id)
        self.assertEqual(data["room"]["id"], self.room2.id)
        self.assertEqual(data["room"]["name"], self.room2.name)
        self.assertEqual(data["room"]["capacity"], self.room2.capacity)
        self.assertEqual(data["room"]["price_per_day"], str(self.room2.price_per_day))
        # Проверка дат
        api_start = timezone.datetime.fromisoformat(data["date_start"])
        api_end = timezone.datetime.fromisoformat(data["date_end"])
        self.assertEqual(api_start, self.start2)
        self.assertEqual(api_end, self.end2)

    def test_get_user_rooms_without_auth(self):
        url = reverse("user-all-booking")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_ditail_data_someone_else_user_booking(self):
        self.client.login(username="user", password="54321")
        url = reverse("user-booking", kwargs={"pk": self.booking1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_ditail_data_someone_else_user_booking_admin(self):
        self.client.login(username="admin", password="admin")
        url = reverse("user-booking", kwargs={"pk": self.booking2.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_ditail_data_user_nonexisting_booking(self):
        self.client.login(username="user", password="54321")
        url = reverse("user-booking", kwargs={"pk": 7})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_someone_else_user_booking(self):
        self.client.login(username="user", password="54321")
        url = reverse("user-booking", kwargs={"pk": self.booking1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_booking(self):
        self.client.login(username="user", password="54321")
        url = reverse("user-booking", kwargs={"pk": self.booking2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Booking.objects.filter(id=self.booking2.id).exists())

    def test_delete_user_booking_admin(self):
        self.client.login(username="admin", password="admin")
        url = reverse("user-booking", kwargs={"pk": self.booking2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Booking.objects.filter(id=self.booking2.id).exists())

    def test_get_user_rooms_empty(self):
        self.client.login(username="admin", password="admin")
        url = reverse("user-all-booking")

        Booking.objects.filter(user=self.superuser).delete()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
