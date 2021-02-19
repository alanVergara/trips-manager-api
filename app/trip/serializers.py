from rest_framework import serializers
from main import models


class RouteSerializer(serializers.ModelSerializer):
    """Serializer for Route object"""
    class Meta:
        model = models.Route
        fields = ('id', 'name', 'origin', 'destination',)
        read_only_fields = ('id',)


class BusSerializer(serializers.ModelSerializer):
    """Serializer for Bus object"""
    driver = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.filter(user_type=3),
        allow_null=True
    )
    seats_bus = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = models.Bus
        fields = ('id', 'num_plate', 'driver', 'seats_bus')
        read_only_fields = ('id', 'seats_bus',)

    def create(self, data):
        """Custom creation function, added seats related bus in creation"""
        bus = models.Bus.objects.create(**data)
        user = data.get('created_by')
        for index in range(1, 11):
            models.Seat.objects.create(
                number=index,
                created_by=user,
                bus=bus
            )
        return bus


class SeatSerializer(serializers.ModelSerializer):
    """Serializer for Seat object"""
    bus = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = models.Seat
        fields = ('id', 'number', 'bus')
        read_only_fields = ('id', 'bus', 'number',)


class TripSerializer(serializers.ModelSerializer):
    """Serializer for Trip object"""
    route = serializers.PrimaryKeyRelatedField(
        queryset=models.Route.objects.all()
    )
    bus = serializers.PrimaryKeyRelatedField(
        queryset=models.Bus.objects.all()
    )
    tickets_trip = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = models.Trip
        fields = ('id', 'name', 'begin_at', 'route', 'bus', 'tickets_trip',)
        read_only_fields = ('id', 'tickets_trip',)

    def create(self, data):
        """Custom creation function, added tickets related trip in creation"""
        trip = models.Trip.objects.create(**data)
        bus = data.get('bus')
        user = data.get('created_by')

        for seat in models.Seat.objects.filter(bus__id=bus.id):
            models.Ticket.objects.create(
                created_by=user,
                seat=seat,
                trip=trip
            )

        return trip


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for Ticket object"""
    trip = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    seat = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = models.Ticket
        fields = ('id', 'reserved', 'trip', 'seat',)
        read_only_fields = ('id', 'trip', 'seat',)
