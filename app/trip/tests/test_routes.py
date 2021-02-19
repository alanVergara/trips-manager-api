from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from main.models import User, Route
from trip.serializers import RouteSerializer


ROUTES_URL = reverse('trip:route-list')


class PublicRouteTest(TestCase):
    """Tests public available routes requests"""

    def setUp(self):
        self.client = APIClient()
        self.user_admin = User.objects.create(
            username='usernameadmin',
            password='testpass',
            user_type=1,
        )

    def test_login_not_required_route_list(self):
        """Test login is not required to access list route"""
        response = self.client.get(ROUTES_URL)

        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_login_not_required_route_detail(self):
        """Test login is not required to access detail route"""
        route_test_1 = Route.objects.create(
            name='route-test-1',
            created_by=self.user_admin,
            origin='origin-test',
            destination='destination-test'
        )

        path = ROUTES_URL+str(route_test_1.id)+'/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_required_route_create(self):
        """Test login is required to create new route"""
        payload = {
            'name': 'routetest',
            'origin': 'test-origin', 
            'destination': 'test-destination'
        }

        response = self.client.post(ROUTES_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_route_update(self):
        """Test login is required to edit a route"""
        payload = {
            'name': 'rote-updated', 
            'origin': 'test-origin', 
            'destination': 'test-destination'
        }

        response = self.client.put(ROUTES_URL+'1/', payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_route_delete(self):
        """Test login is required to delete a route"""
        response = self.client.delete(ROUTES_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRouteTest(TestCase):
    """Test available route request by logged user"""

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

    def test_route_list_by_passenger(self):
        """Test logged passenger access to list route"""
        route_test_1 = Route.objects.create(
            name='route-test-1',
            created_by=self.user_admin,
            origin='origin-test',
            destination='destination-test'
        )
        route_test_2 = Route.objects.create(
            name='route-test-2',
            created_by=self.user_admin,
            origin='origin-test',
            destination='destination-test'
        )

        self.client.force_authenticate(self.user_passenger)
        response = self.client.get(ROUTES_URL)

        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_route_list_by_driver(self):
        """Test logged driver access to list route"""
        route_test_1 = Route.objects.create(
            name='route-test-1',
            created_by=self.user_admin,
            origin='origin-test',
            destination='destination-test'
        )
        route_test_2 = Route.objects.create(
            name='route-test-2',
            created_by=self.user_admin,
            origin='origin-test',
            destination='destination-test'
        )

        self.client.force_authenticate(self.user_driver)
        response = self.client.get(ROUTES_URL)

        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_route_list_by_admin(self):
        """Test logged admin access to list route"""
        route_test_1 = Route.objects.create(
            name='route-test-1',
            created_by=self.user_admin,
            origin='origin-test',
            destination='destination-test'
        )
        route_test_2 = Route.objects.create(
            name='route-test-2',
            created_by=self.user_admin,
            origin='origin-test',
            destination='destination-test'
        )

        self.client.force_authenticate(self.user_admin)
        response = self.client.get(ROUTES_URL)

        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_route_detail_by_passenger(self):
        """Test logged passenger access to detail route"""
        route_test_1 = Route.objects.create(
            name='route-test-1',
            created_by=self.user_admin,
            origin='origin-test',
            destination='destination-test'
        )

        self.client.force_authenticate(self.user_passenger)
        path = ROUTES_URL+str(route_test_1.id)+'/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_route_detail_by_driver(self):
        """Test logged driver access to detail route"""
        route_test_1 = Route.objects.create(
            name='route-test-1',
            created_by=self.user_admin,
            origin='origin-test',
            destination='destination-test'
        )

        self.client.force_authenticate(self.user_driver)
        path = ROUTES_URL+str(route_test_1.id)+'/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_route_detail_by_admin(self):
        """Test logged admin access to detail route"""
        route_test_1 = Route.objects.create(
            name='route-test-1',
            created_by=self.user_admin,
            origin='origin-test',
            destination='destination-test'
        )

        self.client.force_authenticate(self.user_admin)
        path = ROUTES_URL+str(route_test_1.id)+'/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_route_create_by_passenger(self):
        """Test logged passenger access to create route"""
        payload = {
            'name': 'routetest',
            'origin': 'test-origin', 
            'destination': 'test-destination'
        }

        self.client.force_authenticate(self.user_passenger)
        response = self.client.post(ROUTES_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_route_create_by_driver(self):
        """Test logged driver access to create route"""
        payload = {
            'name': 'routetest',
            'origin': 'test-origin', 
            'destination': 'test-destination'
        }

        self.client.force_authenticate(self.user_driver)
        response = self.client.post(ROUTES_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_route_create_by_admin(self):
        """Test logged admin access to create route"""
        payload = {
            'name': 'routetest',
            'origin': 'test-origin', 
            'destination': 'test-destination'
        }

        self.client.force_authenticate(self.user_admin)
        response = self.client.post(ROUTES_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_route_create_by_admin(self):
            """Test logged admin access to create invalid route"""
            payload = {
                'name': '',
                'origin': -1, 
                'destination': -1
            }

            self.client.force_authenticate(self.user_admin)
            response = self.client.post(ROUTES_URL, payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_route_update_by_passenger(self):
        """Test logged passenger access to update route"""
        payload = {
            'name': 'rote-updated', 
            'origin': 'test-origin', 
            'destination': 'test-destination'
        }

        self.client.force_authenticate(self.user_passenger)
        response = self.client.put(ROUTES_URL+'1/', payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_route_update_by_driver(self):
        """Test logged driver access to update driver"""
        payload = {
            'name': 'rote-updated', 
            'origin': 'test-origin', 
            'destination': 'test-destination'
        }

        self.client.force_authenticate(self.user_driver)
        response = self.client.put(ROUTES_URL+'1/', payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_route_update_by_admin(self):
        """Test logged admin access to update correctly route"""
        route_test_1 = Route.objects.create(
            name='route-test-1',
            created_by=self.user_admin,
            origin='origin-test',
            destination='destination-test'
        )

        payload = {
            'name': 'rote-updated', 
            'origin': 'test-origin', 
            'destination': 'test-destination'
        }

        self.client.force_authenticate(self.user_admin)
        path = ROUTES_URL+str(route_test_1.id)+'/'
        response = self.client.put(path, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_route_update_by_admin(self):
        """Test logged admin access to update invalid route"""
        route_test_1 = Route.objects.create(
            name='route-test-1',
            created_by=self.user_admin,
            origin='origin-test',
            destination='destination-test'
        )

        payload = {
            'name': '', 
            'origin': -1, 
            'destination': -1
        }

        self.client.force_authenticate(self.user_admin)
        path = ROUTES_URL+str(route_test_1.id)+'/'
        response = self.client.put(path, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_route_delete_by_passenger(self):
        """Test logged passenger access to update route"""
        self.client.force_authenticate(self.user_passenger)
        response = self.client.delete(ROUTES_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_route_delete_by_driver(self):
        """Test logged driver access to update route"""
        self.client.force_authenticate(self.user_driver)
        response = self.client.delete(ROUTES_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_route_delete_by_admin(self):
        """Test logged admin access to delete correctly route"""
        route_test_1 = Route.objects.create(
            name='route-test-1',
            created_by=self.user_admin,
            origin='origin-test',
            destination='destination-test'
        )

        self.client.force_authenticate(self.user_admin)
        path = ROUTES_URL+str(route_test_1.id)+'/'
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_route_delete_by_admin(self):
        """Test logged admin access to delete invalid route"""

        self.client.force_authenticate(self.user_admin)
        response = self.client.delete(ROUTES_URL+'1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
