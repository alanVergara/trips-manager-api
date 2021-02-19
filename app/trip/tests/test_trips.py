from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from main.models import Trip, User, Route, Bus
from trip.serializers import TripSerializer


TRIPS_URL = reverse('trip:trip-list')


class PublicTripTest(TestCase):
    """Tests public available trips requests"""

    def setUp(self):
        self.client = APIClient()
        self.user_admin = User.objects.create(
            username='usernameadmin',
            password='testpass',
            user_type=1,
        )
        self.route_test = Route.objects.create(
            name='route-test', 
            origin='origin-test',
            destination='destination-test',
            created_by=self.user_admin
        )
        self.bus_test = Bus.objects.create(
            num_plate='NNNN11-test',
            created_by=self.user_admin
        )

    def test_login_not_required_trip_list(self):
        """Test login is not required to access list trip"""
        response = self.client.get(TRIPS_URL)

        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_login_not_required_trip_detail(self):
        """Test login is not required to access detail trip"""
        trip_test_1 = Trip.objects.create(
            name='trip-test-1',
            begin_at=timezone.now(),
            created_by=self.user_admin,
            route=self.route_test,
            bus=self.bus_test
        )

        path = TRIPS_URL+str(trip_test_1.id)+'/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_required_trip_create(self):
        """Test login is required to create new trip"""
        payload = {
            'name': 'triptest', 
            'begin_at': '2021-01-01T10:00:00',
            'route': 1, 
            'bus': 1
        }

        response = self.client.post(TRIPS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_trip_update(self):
        """Test login is required to edit a trip"""
        payload = {
            'name': 'triptestupdated', 
            'begin_at': '2021-01-01T10:00:00',
            'route': 1, 
            'bus': 1
        }

        response = self.client.put(TRIPS_URL+'1/', payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_required_trip_delete(self):
        """Test login is required to delete a trip"""
        response = self.client.delete(TRIPS_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTripTest(TestCase):
    """Test available trip request by logged user"""

    def setUp(self):
        self.client = APIClient()
        self.user_admin = User.objects.create(
            username='usernameadmin',
            password='testpass',
            user_type=1,
        )
        self.user_driver = User.objects.create(
            username='usernamedriver',
            password='testpass',
            user_type=3,
        )
        self.user_passenger = User.objects.create(
            username='usernamepassenger',
            password='testpass',
            user_type=2,
        )
        self.route_test = Route.objects.create(
            name='route-test', 
            origin='origin-test',
            destination='destination-test',
            created_by=self.user_admin
        )
        self.bus_test = Bus.objects.create(
            num_plate='NNNN11-test',
            created_by=self.user_admin
        )

    def test_trip_list_by_passenger(self):
        """Test logged passenger access to list trip"""
        trip_test_1 = Trip.objects.create(
            name='trip-test-1',
            begin_at=timezone.now(),
            created_by=self.user_admin,
            route=self.route_test,
            bus=self.bus_test
        )
        trip_test_2 = Trip.objects.create(
            name='trip-test-2',
            begin_at=timezone.now(),
            created_by=self.user_admin,
            route=self.route_test,
            bus=self.bus_test
        )

        self.client.force_authenticate(self.user_passenger)
        response = self.client.get(TRIPS_URL)

        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_trip_list_by_driver(self):
        """Test logged driver access to list trip"""
        trip_test_1 = Trip.objects.create(
            name='trip-test-1',
            begin_at=timezone.now(),
            created_by=self.user_admin,
            route=self.route_test,
            bus=self.bus_test
        )
        trip_test_2 = Trip.objects.create(
            name='trip-test-2',
            begin_at=timezone.now(),
            created_by=self.user_admin,
            route=self.route_test,
            bus=self.bus_test
        )

        self.client.force_authenticate(self.user_driver)
        response = self.client.get(TRIPS_URL)

        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_trip_list_by_admin(self):
        """Test logged admin access to list trip"""
        trip_test_1 = Trip.objects.create(
            name='trip-test-1',
            begin_at=timezone.now(),
            created_by=self.user_admin,
            route=self.route_test,
            bus=self.bus_test
        )
        trip_test_2 = Trip.objects.create(
            name='trip-test-2',
            begin_at=timezone.now(),
            created_by=self.user_admin,
            route=self.route_test,
            bus=self.bus_test
        )

        self.client.force_authenticate(self.user_admin)
        response = self.client.get(TRIPS_URL)

        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_trip_detail_by_passenger(self):
        """Test logged passenger access to detail trip"""
        trip_test_1 = Trip.objects.create(
            name='trip-test-1',
            begin_at=timezone.now(),
            created_by=self.user_admin,
            route=self.route_test,
            bus=self.bus_test
        )

        self.client.force_authenticate(self.user_passenger)
        path = TRIPS_URL+str(trip_test_1.id)+'/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_trip_detail_by_driver(self):
        """Test logged driver access to detail trip"""
        trip_test_1 = Trip.objects.create(
            name='trip-test-1',
            begin_at=timezone.now(),
            created_by=self.user_admin,
            route=self.route_test,
            bus=self.bus_test
        )

        self.client.force_authenticate(self.user_driver)
        path = TRIPS_URL+str(trip_test_1.id)+'/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_trip_detail_by_admin(self):
        """Test logged admin access to detail trip"""
        trip_test_1 = Trip.objects.create(
            name='trip-test-1',
            begin_at=timezone.now(),
            created_by=self.user_admin,
            route=self.route_test,
            bus=self.bus_test
        )

        self.client.force_authenticate(self.user_admin)
        path = TRIPS_URL+str(trip_test_1.id)+'/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_trip_create_by_passenger(self):
        """Test logged passenger access to create trip"""
        payload = {
            'name': 'triptest', 
            'begin_at': '2021-01-01T10:00:00',
            'route': self.route_test.id, 
            'bus': self.bus_test.id,
            'created_by': self.user_passenger
        }

        self.client.force_authenticate(self.user_passenger)
        response = self.client.post(TRIPS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_trip_create_by_driver(self):
        """Test logged driver access to create trip"""
        payload = {
            'name': 'triptest', 
            'begin_at': '2021-01-01T10:00:00',
            'route': self.route_test.id, 
            'bus': self.bus_test.id,
            'created_by': self.user_driver
        }

        self.client.force_authenticate(self.user_driver)
        response = self.client.post(TRIPS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_trip_create_by_admin(self):
        """Test logged admin access to create correctly trip"""
        payload = {
            'name': 'triptest', 
            'begin_at': '2021-01-01T10:00:00',
            'route': self.route_test.id, 
            'bus': self.bus_test.id,
            'created_by': self.user_admin
        }

        self.client.force_authenticate(self.user_admin)
        response = self.client.post(TRIPS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_invalid_trip_create_by_admin(self):
        """Test logged admin access to create invalid trip"""
        payload = {
            'name': '', 
            'begin_at': '',
            'route': -1, 
            'bus': -1,
            'created_by': self.user_admin
        }

        self.client.force_authenticate(self.user_admin)
        response = self.client.post(TRIPS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_trip_update_by_passenger(self):
        """Test logged passenger access to update trip"""
        payload = {
            'name': 'triptestupdated', 
            'begin_at': '2021-01-01T10:00:00',
            'route': 1, 
            'bus': 1
        }

        self.client.force_authenticate(self.user_passenger)
        response = self.client.put(TRIPS_URL+'1/', payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_trip_update_by_driver(self):
        """Test logged driver access to update trip"""
        payload = {
            'name': 'triptestupdated', 
            'begin_at': '2021-01-01T10:00:00',
            'route': 1, 
            'bus': 1
        }

        self.client.force_authenticate(self.user_driver)
        response = self.client.put(TRIPS_URL+'1/', payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_trip_update_by_admin(self):
        """Test logged admin access to update correctly trip"""
        trip_test_1 = Trip.objects.create(
            name='trip-test-1',
            begin_at=timezone.now(),
            created_by=self.user_admin,
            route=self.route_test,
            bus=self.bus_test
        )

        payload = {
            'name': 'triptestupdated', 
            'begin_at': '2021-01-01T10:00:00',
            'route': 1, 
            'bus': 1
        }

        self.client.force_authenticate(self.user_admin)
        path = TRIPS_URL+str(trip_test_1.id)+'/'
        response = self.client.put(path, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_trip_update_by_admin(self):
        """Test logged admin access to update invalid trip"""
        trip_test_1 = Trip.objects.create(
            name='trip-test-1',
            begin_at=timezone.now(),
            created_by=self.user_admin,
            route=self.route_test,
            bus=self.bus_test
        )

        payload = {
            'name': '', 
            'begin_at': '',
            'route': '', 
            'bus': ''
        }

        self.client.force_authenticate(self.user_admin)
        path = TRIPS_URL+str(trip_test_1.id)+'/'
        response = self.client.put(path, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_trip_delete_by_passenger(self):
        """Test logged passenger access to update trip"""
        self.client.force_authenticate(self.user_passenger)
        response = self.client.delete(TRIPS_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_trip_delete_by_driver(self):
        """Test logged driver access to update trip"""
        self.client.force_authenticate(self.user_driver)
        response = self.client.delete(TRIPS_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_trip_delete_by_admin(self):
        """Test logged admin access to delete correctly trip"""
        trip_test_1 = Trip.objects.create(
            name='trip-test-1',
            begin_at=timezone.now(),
            created_by=self.user_admin,
            route=self.route_test,
            bus=self.bus_test
        )

        self.client.force_authenticate(self.user_admin)
        path = TRIPS_URL+str(trip_test_1.id)+'/'
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_trip_delete_by_admin(self):
        """Test logged admin access to delete invalid trip"""

        self.client.force_authenticate(self.user_admin)
        response = self.client.delete(TRIPS_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
