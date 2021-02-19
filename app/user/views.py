from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from user.serializers import UserSerializer, PassengerLoginSerializer, \
                            PassengerRegisterSerializer, \
                            DriverLoginSerializer, \
                            DriverRegisterSerializer, AdminLoginSerializer
from main.models import User
from user.permissions import IsPassengerOrAdmin, IsDriverOrAdmin


def login_by_user_type(self, request, current_serializer):
    """Complementary function for manage login by serializer"""
    serializer = current_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, token = serializer.save()
    data = {
        'user': UserSerializer(user).data,
        'token': token
    }
    return Response(data, status=status.HTTP_200_OK)


def register_by_user_type(self, request, current_serializer):
    """Complementary function for manage register by serializer"""
    serializer = current_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    data = UserSerializer(user).data
    return Response(data, status=status.HTTP_201_CREATED)


class PassengerViewSet(viewsets.ModelViewSet):
    """Manage passenger actions in database"""
    queryset = User.objects.filter(user_type=2)
    serializer_class = UserSerializer
    permission_classes = [IsPassengerOrAdmin]

    @action(
        methods=['post'],
        detail=False,
        permission_classes=[~permissions.IsAuthenticated]
    )
    def login(self, request):
        """Manage login passenger"""
        return login_by_user_type(self, request, PassengerLoginSerializer)

    def create(self, request):
        """Manage creation of passenger"""
        return register_by_user_type(
            self,
            request,
            PassengerRegisterSerializer
        )


class DriverViewSet(viewsets.ModelViewSet):
    """Manage driver actions in database"""
    queryset = User.objects.filter(user_type=3)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsDriverOrAdmin]

    @action(
        methods=['post'],
        detail=False,
        permission_classes=[~permissions.IsAuthenticated]
    )
    def login(self, request):
        """Manage login driver"""
        return login_by_user_type(self, request, DriverLoginSerializer)

    def create(self, request):
        """Manage creation driver"""
        return register_by_user_type(self, request, DriverRegisterSerializer)


class AdminViewSet(viewsets.GenericViewSet):
    """Manage admin actions in database"""
    queryset = User.objects.filter(user_type=1)
    serializer_class = UserSerializer

    @action(
        methods=['post'],
        detail=False,
        permission_classes=[~permissions.IsAuthenticated]
    )
    def login(self, request):
        """Manage login admin"""
        return login_by_user_type(self, request, AdminLoginSerializer)
