from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from main.models import Trip, User, Route, Bus, Seat, Ticket
from trip.serializers import TicketSerializer


TICKETS_URL = reverse('trip:ticket-list')

class PublicTicketTest(TestCase):
    """Tests public available tickets requests"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required_tickets_list(self):
        """Test login is required to access list ticket"""
        response = self.client.get(TICKETS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_ticket_detail(self):
        """Test login is required to access detail ticket"""
        path = TICKETS_URL+'1/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_ticket_create(self):
        """Test login is required to create new ticket"""
        payload = {
            'seat': 1,
            'passenger': 1, 
            'trip': 1
        }

        response = self.client.post(TICKETS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_ticket_update(self):
        """Test login is required to edit a ticket"""
        payload = {
            'seat': 1,
            'passenger': 1, 
            'trip': 1
        }

        response = self.client.put(TICKETS_URL+'1/', payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_ticket_delete(self):
        """Test login is required to delete a ticket"""
        response = self.client.delete(TICKETS_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTicketTest(TestCase):
    """Test available ticket request by logged user"""

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
        self.trip_test = Trip.objects.create(
            name='trip-test',
            begin_at=timezone.now(),
            created_by=self.user_admin,
            route=self.route_test,
            bus=self.bus_test
        )
        self.seat_test = Seat.objects.create(
            number=1,
            created_by=self.user_admin,
            bus=self.bus_test
        )

    def test_ticket_list_by_passenger(self):
        """Test logged passenger access to list ticket"""
        ticket_test_1 = Ticket.objects.create(
            created_by=self.user_admin,
            trip=self.trip_test,
            seat=self.seat_test
        )
        ticket_test_2 = Ticket.objects.create(
            created_by=self.user_admin,
            trip=self.trip_test,
            seat=self.seat_test
        )

        self.client.force_authenticate(self.user_passenger)
        response = self.client.get(TICKETS_URL)

        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_ticket_list_by_driver(self):
        """Test logged driver access to list ticket"""
        self.client.force_authenticate(self.user_driver)
        response = self.client.get(TICKETS_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ticket_list_by_admin(self):
        """Test logged admin access to list ticket"""
        self.client.force_authenticate(self.user_admin)
        response = self.client.get(TICKETS_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ticket_detail_by_passenger(self):
        """Test logged passenger access to detail ticket"""
        ticket_test_1 = Ticket.objects.create(
            created_by=self.user_admin,
            trip=self.trip_test,
            seat=self.seat_test
        )

        self.client.force_authenticate(self.user_passenger)
        path = TICKETS_URL+str(ticket_test_1.id)+'/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ticket_detail_by_driver(self):
        """Test logged driver access to detail ticket"""
        self.client.force_authenticate(self.user_driver)
        path = TICKETS_URL+'1/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ticket_detail_by_admin(self):
        """Test logged admin access to detail ticket"""
        self.client.force_authenticate(self.user_admin)
        path = TICKETS_URL+'1/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ticket_create_by_passenger(self):
        """Test logged passenger access to create ticket"""
        payload = {
            'seat': 1,
            'passenger': 1, 
            'trip': 1
        }

        self.client.force_authenticate(self.user_passenger)
        response = self.client.post(TICKETS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ticket_create_by_driver(self):
        """Test logged driver access to create ticket"""
        payload = {
            'seat': 1,
            'passenger': 1, 
            'trip': 1
        }

        self.client.force_authenticate(self.user_driver)
        response = self.client.post(TICKETS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ticket_create_by_admin(self):
        """Test logged admin access to create ticket"""
        payload = {
            'seat': 1,
            'passenger': 1, 
            'trip': 1
        }

        self.client.force_authenticate(self.user_admin)
        response = self.client.post(TICKETS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ticket_update_by_passenger(self):
        """Test logged passenger access to update correctly ticket"""
        ticket_test_1 = Ticket.objects.create(
            created_by=self.user_admin,
            trip=self.trip_test,
            seat=self.seat_test
        )
        payload = {
            'reserved': True
        }

        self.client.force_authenticate(self.user_passenger)
        path = TICKETS_URL+str(ticket_test_1.id)+'/'
        response = self.client.put(path, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_ticket_update_by_passenger(self):
        """Test logged passenger access to update invalid ticket"""
        ticket_test_1 = Ticket.objects.create(
            created_by=self.user_admin,
            trip=self.trip_test,
            seat=self.seat_test
        )
        payload = {
            'reserved': -1
        }

        self.client.force_authenticate(self.user_passenger)
        path = TICKETS_URL+str(ticket_test_1.id)+'/'
        response = self.client.put(path, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ticket_update_by_driver(self):
        """Test logged driver access to update ticket"""
        payload = {
            'reserved': True
        }

        self.client.force_authenticate(self.user_driver)
        response = self.client.put(TICKETS_URL+'1/', payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ticket_update_by_admin(self):
        """Test logged admin access to update ticket"""
        payload = {
            'reserved': True
        }

        self.client.force_authenticate(self.user_admin)
        response = self.client.put(TICKETS_URL+'1/', payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ticket_delete_by_passenger(self):
        """Test logged passenger access to update ticket"""
        self.client.force_authenticate(self.user_passenger)
        response = self.client.delete(TICKETS_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ticket_delete_by_driver(self):
        """Test logged driver access to update ticket"""
        self.client.force_authenticate(self.user_driver)
        response = self.client.delete(TICKETS_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ticket_delete_by_admin(self):
        """Test logged admin access to update ticket"""
        self.client.force_authenticate(self.user_admin)
        response = self.client.delete(TICKETS_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
