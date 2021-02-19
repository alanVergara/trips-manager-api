from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q, Count

from main import models
from trip import serializers
from trip.permissions import IsAdminRoute, IsAdminBus, \
                            IsPassengerTicket, IsAdminProfile


def add_passenger_average(route):
    """Complementary function for get average of passengers in route"""
    average = 0
    route_quantity = models.Trip.objects.filter(
        route__id=route.get('id')
    ).count()
    route_passengers = models.Trip.objects.filter(
        tickets_trip__reserved=True
    ).count()

    if route_quantity > 0:
        average = route_passengers/route_quantity
    route['average'] = round(average, 4)
    return route


def percentage_buses_use_by_route(bus, route_id, percentage):
    """Complementary function for get percentage of usage buses"""
    buses = []
    pctage = models.Trip.objects.filter(
        bus__id=bus.get('id'),
        route__id=route_id
    ).annotate(
        pctage=Count(
            'tickets_trip',
            filter=Q(tickets_trip__reserved=True)
        ) * 100/Count('tickets_trip')
    ).filter(
        pctage__gt=percentage
    )

    for bus_per in pctage:
        bus["use_percentage"] = bus_per.pctage
        buses.append(bus)

    return buses


class RouteViewSet(viewsets.ModelViewSet):
    """Manage route actions in database"""
    queryset = models.Route.objects.all()
    serializer_class = serializers.RouteSerializer
    permission_classes = [IsAdminRoute]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(methods=['get'], detail=False, permission_classes=[IsAdminProfile])
    def average_passengers(self, request):
        """Getting average passengers"""
        data = []
        serializer = self.serializer_class(self.queryset, many=True)
        for route in serializer.data:
            data.append(add_passenger_average(route))

        return Response(data, status=status.HTTP_200_OK)


class BusViewSet(viewsets.ModelViewSet):
    """Manage bus actions in database"""
    queryset = models.Bus.objects.all()
    serializer_class = serializers.BusSerializer
    permission_classes = [IsAdminBus]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(methods=['get'], detail=False, permission_classes=[IsAdminProfile])
    def use_by_route(self, request):
        """Getting use percentage of route"""
        data = []
        route_id = request.query_params.get('route_id')
        percentage = request.query_params.get('percentage')
        serializer = self.serializer_class(self.queryset, many=True)
        for bus in serializer.data:
            tmp_buses = percentage_buses_use_by_route(
                bus,
                route_id,
                percentage
            )
            data = data + tmp_buses

        return Response(data, status=status.HTTP_200_OK)


class SeatViewSet(viewsets.ModelViewSet):
    """Manage seat actions in database"""
    queryset = models.Seat.objects.all()
    serializer_class = serializers.SeatSerializer
    permission_classes = [IsPassengerTicket]


class TripViewSet(viewsets.ModelViewSet):
    """Manage trip actions in database"""
    queryset = models.Trip.objects.all()
    serializer_class = serializers.TripSerializer
    permission_classes = [IsAdminRoute]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    """Manage ticket actions in database"""
    queryset = models.Ticket.objects.all()
    serializer_class = serializers.TicketSerializer
    permission_classes = [IsPassengerTicket]

    def perform_update(self, serializer):
        if self.request.data.get('reserved', False):
            serializer.save(passenger=self.request.user)
