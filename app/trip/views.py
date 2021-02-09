from rest_framework import viewsets
from main import models
from trip import serializers
from rest_framework import permissions


class RouterViewSet(viewsets.ModelViewSet):
    """"""
    queryset = models.Route.objects.all()
    serializer_class = serializers.RouteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BusViewSet(viewsets.ModelViewSet):
    """"""
    queryset = models.Bus.objects.all()
    serializer_class = serializers.BusSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(driver=self.request.driver)


class SeatViewSet(viewsets.ModelViewSet):
    """"""
    queryset = models.Seat.objects.all()
    serializer_class = serializers.SeatSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(passenger=self.request.passenger)


class TripViewSet(viewsets.ModelViewSet):
    """"""
    queryset = models.Trip.objects.all()
    serializer_class = serializers.TripSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
