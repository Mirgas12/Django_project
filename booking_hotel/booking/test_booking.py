import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "booking_hotel.settings")
import django
django.setup()

import pytest
from rest_framework.test import APIClient
from booking.models import Room, Booking

@pytest.mark.django_db
def test_create_room():
    client = APIClient()
    response = client.post("/rooms/create/", {
        "description": "Тестовый номер",
        "price_per_night": 2000
    })
    assert response.status_code == 201
    assert "room_id" in response.data

@pytest.mark.django_db
def test_list_rooms_sorted_by_price():
    Room.objects.create(description="A", price_per_night=1000)
    Room.objects.create(description="B", price_per_night=3000)
    client = APIClient()
    response = client.get("/rooms/list/?sort_by=price&order=desc")  # Исправленный путь!
    assert response.status_code == 200
    data = response.data
    assert len(data) >= 2
    assert data[0]['price_per_night'] >= data[1]['price_per_night']

@pytest.mark.django_db
def test_create_booking_and_overlap():
    client = APIClient()
    room = Room.objects.create(description="Test", price_per_night=1500)
    response1 = client.post("/bookings/create/", {
        "room": room.id,
        "date_start": "2024-06-10",
        "date_end": "2024-06-12"
    })
    assert response1.status_code == 201
    response2 = client.post("/bookings/create/", {
        "room": room.id,
        "date_start": "2024-06-11",
        "date_end": "2024-06-13"
    })
    assert response2.status_code == 400

@pytest.mark.django_db
def test_delete_booking():
    client = APIClient()
    room = Room.objects.create(description="Test", price_per_night=1000)
    booking = Booking.objects.create(room=room, date_start="2024-06-10", date_end="2024-06-12")
    response = client.delete(f"/bookings/{booking.id}/delete/")
    assert response.status_code == 204
    assert not Booking.objects.filter(id=booking.id).exists()

@pytest.mark.django_db
def test_list_bookings_sorted():
    client = APIClient()
    room = Room.objects.create(description="Test", price_per_night=1000)
    Booking.objects.create(room=room, date_start="2024-06-15", date_end="2024-06-16")
    Booking.objects.create(room=room, date_start="2024-06-10", date_end="2024-06-12")
    response = client.get(f"/bookings/list/?room_id={room.id}")  # <-- исправлено!
    assert response.status_code == 200
    data = response.data
    assert data[0]['date_start'] <= data[1]['date_start']

