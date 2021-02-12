from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    """Custom user that support multiple types"""
    TYPES = (
        (1, 'Admin'),
        (2, 'Passenger'),
        (3, 'Driver'),
    )
    user_type = models.PositiveSmallIntegerField(choices=TYPES, default=2)


class Route(models.Model):
    """Route to be used for define way to go"""
    name = models.CharField(max_length=120)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='routes',
    )

    def __str__(self):
        return self.name


class Bus(models.Model):
    """Bus to be used to travel a route with passengers"""
    num_plate = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='buses',
    )
    driver = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return self.num_plate


class Seat(models.Model):
    """Seat to be used in bus"""
    number = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='seats_admin',
    )
    bus = models.ForeignKey(
        'Bus',
        on_delete=models.CASCADE,
        related_name='seats_bus',
    )


class Trip(models.Model):
    """Trip to be used for define bus and passengers traveling in a route"""
    begin_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=120)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='trips_admin',
    )
    route = models.ForeignKey(
        'Route',
        on_delete=models.CASCADE,
        related_name='trips_route',
    )
    bus = models.ForeignKey(
        'Bus',
        on_delete=models.CASCADE,
        related_name='trips_bus',
    )

    def __str__(self):
        return self.name


class Ticket(models.Model):
    """Ticket to be used in trip"""
    created_at = models.DateTimeField(auto_now_add=True)
    reserved = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets_admin',
    )
    trip = models.ForeignKey(
        'Trip',
        on_delete=models.CASCADE,
        related_name='tickets_trip',
    )
    passenger = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets_passenger',
        null=True,
    )
    seat = models.ForeignKey(
        'Seat',
        on_delete=models.CASCADE,
        related_name='tickets_seat',
    )

    def __str__(self):
        return self.id
