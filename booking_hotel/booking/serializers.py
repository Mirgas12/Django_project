from rest_framework import serializers
from .models import Room, Booking


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'description', 'price_per_night', 'added_at']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'room', 'date_start', 'date_end']

    def validate(self, data):
        if data['date_start'] >= data['date_end']:
            raise serializers.ValidationError("date_start должна быть раньше date_end")
        overlaps = Booking.objects.filter(
            room=data['room'],
            date_start__lt=data['date_end'],
            date_end__gt=data['date_start']
        ).exists()
        if overlaps:
            raise serializers.ValidationError("Room already booked for these dates")
        return data