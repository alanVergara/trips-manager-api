from rest_framework import serializers
from main import models


class RouteSerializer(serializers.ModelSerializer):
    """Serializer for Route object"""
    class Meta:
        model = models.Route
        fields = ('id', 'origin', 'destination',)
        read_only_fields = ('id',)


class BusSerializer(serializers.ModelSerializer):
    """Serializer for Bus object"""
    driver = serializers.ReadOnlyField(source='driver')
    class Meta:
        model = models.Bus
        fields = ('id', 'num_plate', 'driver')
        read_only_fields = ('id')


class SeatSerializer(serializers.ModelSerializer):
    """Serializer for Seat object"""
    passenger = serializers.ReadOnlyField(source='passenger')
    bus = BusSerializer()
    class Meta:
        model = models.Seat
        fields = ('id', 'number', 'passenger', 'bus')
        read_only_fields = ('id')


class TripSerializer():
    """Serializer for Trip object"""
    route = RouteSerializer()
    bus = BusSerializer()
    class Meta:
        model = models.Trip
        fields = ('id', 'begin_at', 'route', 'bus')
