from django.urls import path
from booking.views import create_booking, delete_booking, list_bookings

urlpatterns = [
    path('create/', create_booking),
    path('<int:booking_id>/delete/', delete_booking),
    path('list/',list_bookings),
]