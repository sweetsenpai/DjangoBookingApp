from datetime import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

import pytest

from core.models import Room


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class UserCreateBookingApiTest(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(username="user", password="54321")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.room1 = Room.objects.create(
            name="Для двоих", price_per_day=Decimal("100.00"), capacity=2
        )

    def test_create_booking(self):
        url = reverse("booking-list")
        data = {
            "room": self.room1.id,
            "date_start": datetime.now() + timezone.timedelta(days=1),
            "date_end": datetime.now() + timezone.timedelta(days=2),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["room"], self.room1.id)

    def test_create_booking_without_auth(self):
        self.client.logout()
        url = reverse("booking-list")
        data = {
            "room": self.room1.id,
            "date_start": datetime.now() + timezone.timedelta(days=1),
            "date_end": datetime.now() + timezone.timedelta(days=2),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_booking_with_wrong_data(self):
        url = reverse("booking-list")
        data = {
            "room": self.room1.id,
            "date_start": datetime.now() + timezone.timedelta(days=1),
            "date_end": datetime.now() - timezone.timedelta(days=2),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_overlaping_booking(self):
        url = reverse("booking-list")
        data = {
            "room": self.room1.id,
            "date_start": datetime.now() + timezone.timedelta(days=1),
            "date_end": datetime.now() + timezone.timedelta(days=2),
        }
        self.client.post(url, data)
        error_response = self.client.post(url, data)
        self.assertEqual(error_response.status_code, status.HTTP_409_CONFLICT)
