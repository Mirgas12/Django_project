from django.urls import path
from booking.views import create_room, delete_room, list_rooms

urlpatterns = [
    path('create/', create_room),
    path('<int:room_id>/delete/', delete_room),
    path('list/',list_rooms),
]
