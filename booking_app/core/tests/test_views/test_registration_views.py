from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

import pytest


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class RegistrationApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_valid_registration(self):
        url = reverse("user-list")

        data = {
            "username": "test_user",
            "password": "test_password_99",
            "password2": "test_password_99",
            "email": "test_email@test.com",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_registration_unmatching_passwords(self):
        url = reverse("user-list")

        data = {
            "username": "test_user",
            "password": "test_password_99",
            "password2": "test_password_100",
            "email": "test_email@test.com",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_registration_username_exists(self):
        url = reverse("user-list")

        data = {
            "username": "test_user",
            "password": "test_password_99",
            "password2": "test_password_99",
        }
        self.client.post(url, data)
        error_response = self.client.post(url, data)
        self.assertEqual(error_response.status_code, status.HTTP_400_BAD_REQUEST)
