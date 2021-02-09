from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from user.serializers import UserSerializer, PassengerLoginSerializer, \ 
                            PassengerRegisterSerializer, DriverLoginSerializer \
                            DriverRegisterSerializer, AdminLoginSerializer
from main.models import User


def login_by_user_type(self, request, current_serializer):
    """"""
    serializer = current_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, token = serializer.save()
    data = {
        'user': UserSerializer(user).data,
        'token': token
    }
    return Response(data, status=status.HTTP_201_CREATED)

def register_by_user_type(self, request, current_serializer):
    """"""
    serializer = current_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    data = UserSerializer(user).data
    return Response(data, status=status.HTTP_201_CREATED)


class PassengerViewSet(viewsets.GenericViewSet):
    """"""
    queryset = User.objects.filter(user_type=2)
    serializer_class = UserSerializer

    @action(methods=['post'], detail=False)
    def login(self, request):
        """"""
        return login_by_user_type(self, request, PassengerLoginSerializer)

    @action(methods=['post'], detail=False)
    def register(self, request):
        """"""
        return register_by_user_type(self, request, PassengerRegisterSerializer)


class DriverViewSet(viewsets.GenericViewSet):
    """"""
    queryset = User.objects.filter(user_type=3)
    serializer_class = UserSerializer

    @action(methods=['post'], detail=False)
    def login(self, request):
        """"""
        return login_by_user_type(self, request, DriverLoginSerializer)

    @action(methods=['post'], detail=False)
    def register(self, request):
        """"""
        return register_by_user_type(self, request, DriverRegisterSerializer)


class AdminViewSet(viewsets.GenericViewSet):
    """"""
    queryset = User.objects.filter(user_type=3)
    serializer_class = UserSerializer

    @action(methods=['post'], detail=False)
    def login(self, request):
        """"""
        return login_by_user_type(self, request, AdminLoginSerializer)
