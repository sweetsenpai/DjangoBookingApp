from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

import pytest

from booking_app_admin.models import Room


class ShowRoomsApiTest(APITestCase):
    @pytest.mark.django_db
    def setUp(self):
        rooms = [
            Room(name="Для двоих", price_per_day=Decimal("100.00"), capacity=2),
            Room(name="Для одного", price_per_day=Decimal("50.00"), capacity=1),
            Room(name="Для троих", price_per_day=Decimal("150.00"), capacity=3),
        ]
        Room.objects.bulk_create(rooms)

    @pytest.mark.django_db
    def test_get_rooms(self):
        url = reverse("all-rooms")
        response = self.client.get(url)
        expected_response = [
            {"id": 1, "name": "Для двоих", "price_per_day": "100.00", "capacity": 2},
            {"id": 2, "name": "Для одного", "price_per_day": "50.00", "capacity": 1},
            {"id": 3, "name": "Для троих", "price_per_day": "150.00", "capacity": 3},
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    @pytest.mark.django_db
    def test_get_rooms_with_filter(self):
        url = reverse("all-rooms")
        response = self.client.get(f"{url}?ordering=price_per_day")
        expected_response = [
            {"id": 2, "name": "Для одного", "price_per_day": "50.00", "capacity": 1},
            {"id": 1, "name": "Для двоих", "price_per_day": "100.00", "capacity": 2},
            {"id": 3, "name": "Для троих", "price_per_day": "150.00", "capacity": 3},
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)
