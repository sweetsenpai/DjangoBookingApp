from datetime import datetime
from decimal import Decimal

from django.urls import reverse
from django.utils.timezone import make_aware

import pytest

from booking_app_admin.models import Booking, Room


@pytest.fixture
def test_rooms(db):
    room1 = Room.objects.create(
        name="Для двоих", price_per_day=Decimal("100.00"), capacity=2
    )
    room2 = Room.objects.create(
        name="Для одного", price_per_day=Decimal("50.00"), capacity=1
    )
    return room1, room2


@pytest.fixture
def test_bookings(test_rooms, django_user_model):
    room1, room2 = test_rooms
    superuser = django_user_model.objects.create_superuser(
        username="admin", password="admin"
    )
    user = django_user_model.objects.create_user(username="user", password="54321")

    Booking.objects.create(
        room=room1,
        user=superuser,
        date_start=make_aware(datetime(2021, 1, 1)),
        date_end=make_aware(datetime(2021, 1, 2)),
    )
    Booking.objects.create(
        room=room2,
        user=user,
        date_start=make_aware(datetime(2021, 1, 3)),
        date_end=make_aware(datetime(2021, 1, 4)),
    )
    return superuser, user


@pytest.mark.django_db
def test_free_rooms_available(client, test_bookings, test_rooms):
    url = reverse("search-free-rooms")
    response = client.get(
        url,
        {
            "date_start": "2026-01-02",
            "date_end": "2026-01-03",
            "capacity": 1,
        },
    )

    assert response.status_code == 200
    ids = [r["id"] for r in response.data]
    assert test_rooms[0].id in ids
    assert test_rooms[1].id in ids


@pytest.mark.django_db
def test_free_rooms_capacity_filter(client, test_bookings, test_rooms):
    url = reverse("search-free-rooms")
    response = client.get(
        url,
        {
            "date_start": "2026-01-02",
            "date_end": "2026-01-03",
            "capacity": 2,
        },
    )
    assert response.status_code == 200
    ids = [r["id"] for r in response.data]
    assert test_rooms[0].id in ids
    assert test_rooms[1].id not in ids


@pytest.mark.django_db
def test_free_rooms_validation_error(client):
    url = reverse("search-free-rooms")
    response = client.get(url, {"date_end": "2021-01-03"})
    assert response.status_code == 400
