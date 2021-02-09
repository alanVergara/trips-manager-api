from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from user.serializers import UserSerializer, PassengerLoginSerializer, PassengerRegisterSerializer
from main.models import User


class UserViewSet(viewsets.GenericViewSet):
    """"""
    queryset = User.objects.filter(user_type=2)
    serializer_class = UserSerializer

    @action(methods='POST', detail=False)
    def login(self, request):
        """"""
        serializer = PassengerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserSerializer(user).data,
            'token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(methods='POST', detail=False)
    def signup(self, request):
        """"""
        serializer = PassengerRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

