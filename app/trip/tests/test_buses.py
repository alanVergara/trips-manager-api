from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from main.models import User, Bus
from trip.serializers import BusSerializer


BUSES_URL = reverse('trip:bus-list')


class PublicBusTest(TestCase):
    """Tests public available buses requests"""

    def setUp(self):
        self.client = APIClient()
        self.user_admin = User.objects.create(
            username='usernameadmin',
            password='testpass',
            user_type=1,
        )

    def test_login_required_bus_list(self):
        """Test login is required to access list bus"""
        response = self.client.get(BUSES_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_not_required_bus_detail(self):
        """Test login is not required to access detail bus"""
        bus_test_1 = Bus.objects.create(
            num_plate='NNNN11-test',
            created_by=self.user_admin,
        )

        path = BUSES_URL+str(bus_test_1.id)+'/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_required_bus_create(self):
        """Test login is required to create new bus"""
        payload = {
            'num_plate': 'NNNN11-test'
        }

        response = self.client.post(BUSES_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_bus_update(self):
        """Test login is required to edit a bus"""
        payload = {
            'num_plate': 'NNNN11-updated',
        }

        response = self.client.put(BUSES_URL+'1/', payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_bus_delete(self):
        """Test login is required to delete a bus"""
        response = self.client.delete(BUSES_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBusTest(TestCase):
    """Test available bus request by logged user"""

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

    def test_bus_list_by_passenger(self):
        """Test logged passenger access to list bus"""
        self.client.force_authenticate(self.user_passenger)
        response = self.client.get(BUSES_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bus_list_by_driver(self):
        """Test logged driver access to list bus"""
        self.client.force_authenticate(self.user_driver)
        response = self.client.get(BUSES_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bus_list_by_admin(self):
        """Test logged admin access to list bus"""
        Bus.objects.create(
            num_plate='NNNN11-test-1',
            created_by=self.user_admin,
        )
        Bus.objects.create(
            num_plate='NNNN11-test-2',
            created_by=self.user_admin,
        )

        self.client.force_authenticate(self.user_admin)
        response = self.client.get(BUSES_URL)

        buses = Bus.objects.all()
        serializer = BusSerializer(buses, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_bus_detail_by_passenger(self):
        """Test logged passenger access to detail bus"""
        bus_test_1 = Bus.objects.create(
            num_plate='NNNN11-test-1',
            created_by=self.user_admin,
        )

        self.client.force_authenticate(self.user_passenger)
        path = BUSES_URL+str(bus_test_1.id)+'/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bus_detail_by_driver(self):
        """Test logged driver access to detail bus"""
        bus_test_1 = Bus.objects.create(
            num_plate='NNNN11-test-1',
            created_by=self.user_admin,
        )

        self.client.force_authenticate(self.user_driver)
        path = BUSES_URL+str(bus_test_1.id)+'/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bus_detail_by_admin(self):
        """Test logged admin access to detail bus"""
        bus_test_1 = Bus.objects.create(
            num_plate='NNNN11-test-1',
            created_by=self.user_admin,
        )

        self.client.force_authenticate(self.user_admin)
        path = BUSES_URL+str(bus_test_1.id)+'/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bus_create_by_passenger(self):
        """Test logged passenger access to create bus"""
        payload = {
            'num_plate': 'NNNN11-test'
        }

        self.client.force_authenticate(self.user_passenger)
        response = self.client.post(BUSES_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bus_create_by_driver(self):
        """Test logged driver access to create bus"""
        payload = {
            'num_plate': 'NNNN11-test'
        }

        self.client.force_authenticate(self.user_driver)
        response = self.client.post(BUSES_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bus_create_by_admin(self):
        """Test logged admin access to create correctly bus"""
        payload = {
            'num_plate': 'NNNN11test',
            'driver': self.user_driver.id
        }
        self.client.force_authenticate(self.user_admin)
        response = self.client.post(BUSES_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_bus_create_by_admin(self):
        """Test logged admin access to create invalid bus"""
        payload = {
            'num_plate': '',
            'driver': ''
        }
        self.client.force_authenticate(self.user_admin)
        response = self.client.post(BUSES_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bus_update_by_passenger(self):
        """Test logged passenger access to update bus"""
        payload = {
            'num_plate': 'NNNN11test',
            'driver': self.user_driver.id
        }

        self.client.force_authenticate(self.user_passenger)
        response = self.client.put(BUSES_URL+'1/', payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bus_update_by_driver(self):
        """Test logged driver access to update bus"""
        payload = {
            'num_plate': 'NNNN11test',
            'driver': self.user_driver.id
        }

        self.client.force_authenticate(self.user_driver)
        response = self.client.put(BUSES_URL+'1/', payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bus_update_by_admin(self):
        """Test logged admin access to update correctly bus"""
        bus_test_1 = Bus.objects.create(
            num_plate='NN11-test',
            created_by=self.user_admin,
        )

        payload = {
            'num_plate': 'NNNN11upd',
            'driver': self.user_driver.id
        }

        self.client.force_authenticate(self.user_admin)
        path = BUSES_URL+str(bus_test_1.id)+'/'
        response = self.client.put(path, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_bus_update_by_admin(self):
        """Test logged admin access to update invalid bus"""
        bus_test_1 = Bus.objects.create(
            num_plate='NN11-test',
            created_by=self.user_admin,
        )

        payload = {
            'num_plate': '',
            'driver': ''
        }

        self.client.force_authenticate(self.user_admin)
        path = BUSES_URL+str(bus_test_1.id)+'/'
        response = self.client.put(path, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bus_delete_by_passenger(self):
        """Test logged passenger access to update bus"""
        self.client.force_authenticate(self.user_passenger)
        response = self.client.delete(BUSES_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bus_delete_by_driver(self):
        """Test logged driver access to update bus"""
        self.client.force_authenticate(self.user_driver)
        response = self.client.delete(BUSES_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bus_delete_by_admin(self):
        """Test logged admin access to delete correctly bus"""
        bus_test_1 = Bus.objects.create(
            num_plate='NN11-test',
            created_by=self.user_admin,
        )

        self.client.force_authenticate(self.user_admin)
        path = BUSES_URL+str(bus_test_1.id)+'/'
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_bus_delete_by_admin(self):
        """Test logged admin access to delete invalid bus"""

        self.client.force_authenticate(self.user_admin)
        response = self.client.delete(BUSES_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
