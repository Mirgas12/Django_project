from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *


@api_view(['POST'])
def create_room(request):
    serializer = RoomSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    room = serializer.save()
    return Response({"room_id": room.id}, status=status.HTTP_201_CREATED)

@api_view(["DELETE"])
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def list_rooms(request):
    sort_by = request.GET.get('sort_by', "added")
    order = request.GET.get('order','asc')
    if sort_by not in ('price', 'added'):
        return Response({"error": "Invalid sort_by param"}, status=400)
    field = 'price_per_night' if sort_by == 'price' else 'added_at'
    if order == 'desc':
        field = f'-{field}'
    rooms = Room.objects.all().order_by(field)
    data = RoomSerializer(rooms, many=True).data
    return Response(data)

@api_view(['POST'])
def create_booking(request):
    serializer = BookingSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    booking = serializer.save()
    return Response({"booking_id": booking.id}, status=status.HTTP_201_CREATED)

@api_view(["DELETE"])
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def list_bookings(request):
    room_id = request.GET.get("room_id")
    room = get_object_or_404(Room, id=room_id)
    bookings = room.bookings.all().order_by('date_start')
    data = [
        {
            'booking_id': b.id,
            'date_start': str(b.date_start),
            'date_end': str(b.date_end)
        } for b in bookings
    ]
    return Response(data)