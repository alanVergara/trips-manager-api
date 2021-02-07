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
    user_type = models.PositiveSmallIntegerField(choices=TYPES)


class Route(models.Model):
    """Route to be used for define way to go"""
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='routes',
    )


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
    )


class Seat(models.Model):
    """Seat to be used in bus"""
    number = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='seats_admin',
    )
    passenger = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='seats_passenger',
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
