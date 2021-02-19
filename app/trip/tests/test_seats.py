from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from main.models import User, Seat, Bus
from trip.serializers import SeatSerializer


SEATS_URL = reverse('trip:seat-list')


class PublicSeatTest(TestCase):
    """Tests public available seats requests"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required_seats_list(self):
        """Test login is required to access list seat"""
        response = self.client.get(SEATS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_seat_detail(self):
        """Test login is required to access detail seat"""
        path = SEATS_URL+'1/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_seat_create(self):
        """Test login is required to create new seat"""
        payload = {
            'number': 1,
            'bus': 1
        }
        response = self.client.post(SEATS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_seat_update(self):
        """Test login is required to edit a seat"""
        payload = {
            'number': 1,
            'bus': 1
        }

        response = self.client.put(SEATS_URL+'1/', payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_seat_delete(self):
        """Test login is required to delete a seat"""
        response = self.client.delete(SEATS_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateSeatTest(TestCase):
    """Test available seats request by logged user"""

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
        self.bus_test = Bus.objects.create(
            num_plate='NNNN11-test',
            created_by=self.user_admin
        )

    def test_seat_list_by_passenger(self):
        """Test logged passenger access to list seat"""
        Seat.objects.create(
            created_by=self.user_admin,
            number=1,
            bus=self.bus_test
        )
        Seat.objects.create(
            created_by=self.user_admin,
            number=2,
            bus=self.bus_test
        )

        self.client.force_authenticate(self.user_passenger)
        response = self.client.get(SEATS_URL)

        seats = Seat.objects.all()
        serializer = SeatSerializer(seats, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_seat_list_by_driver(self):
        """Test logged driver access to list seat"""
        self.client.force_authenticate(self.user_driver)
        response = self.client.get(SEATS_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seat_list_by_admin(self):
        """Test logged admin access to list seat"""
        self.client.force_authenticate(self.user_admin)
        response = self.client.get(SEATS_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seat_detail_by_passenger(self):
        """Test logged passenger access to detail seat"""
        seat_test_1 = Seat.objects.create(
            created_by=self.user_admin,
            number=1,
            bus=self.bus_test
        )

        self.client.force_authenticate(self.user_passenger)
        path = SEATS_URL+str(seat_test_1.id)+'/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_seat_detail_by_driver(self):
        """Test logged driver access to detail seat"""
        self.client.force_authenticate(self.user_driver)
        path = SEATS_URL+'1/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seat_detail_by_admin(self):
        """Test logged admin access to detail seat"""
        self.client.force_authenticate(self.user_admin)
        path = SEATS_URL+'1/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seat_create_by_passenger(self):
        """Test logged passenger access to create seat"""
        payload = {
            'number': 1,
            'bus': 1
        }

        self.client.force_authenticate(self.user_passenger)
        response = self.client.post(SEATS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seat_create_by_driver(self):
        """Test logged driver access to create seat"""
        payload = {
            'number': 1,
            'bus': 1
        }

        self.client.force_authenticate(self.user_driver)
        response = self.client.post(SEATS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seat_create_by_admin(self):
        """Test logged admin access to create seat"""
        payload = {
            'number': 1,
            'bus': 1
        }

        self.client.force_authenticate(self.user_admin)
        response = self.client.post(SEATS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seat_update_by_driver(self):
        """Test logged driver access to update seat"""
        payload = {
            'reserved': True
        }

        self.client.force_authenticate(self.user_driver)
        response = self.client.put(SEATS_URL+'1/', payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seat_update_by_admin(self):
        """Test logged admin access to update seat"""
        payload = {
            'reserved': True
        }

        self.client.force_authenticate(self.user_admin)
        response = self.client.put(SEATS_URL+'1/', payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seat_delete_by_passenger(self):
        """Test logged passenger access to update seat"""
        self.client.force_authenticate(self.user_passenger)
        response = self.client.delete(SEATS_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seat_delete_by_driver(self):
        """Test logged driver access to update seat"""
        self.client.force_authenticate(self.user_driver)
        response = self.client.delete(SEATS_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seat_delete_by_admin(self):
        """Test logged admin access to update seat"""
        self.client.force_authenticate(self.user_admin)
        response = self.client.delete(SEATS_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
