from django.contrib.auth import password_validation, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from main.models import User


class UserSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = User
        fields = ('username', 'password', 'user_type')
        extra_kwargs = {'password': {'write_only': True}}


class PassengerLoginSerializer(serializers.Serializer):
    """"""
    username = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """"""
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            message = 'El usuario o contraseña es incorrecto.'
            raise serializers.ValidationError(message)
        data['user'] = user
        return data

    def create(self, data):
        """"""
        token, created = Token.objects.get_or_create(user=data['user'])
        return data['user'], token.key


class PassengerRegisterSerializer(serializers.Serializer):
    """"""
    username = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirm = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """"""
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        if password != password_confirm:
            message = 'Las contraseñas no coinciden.'
            raise serializers.ValidationError(message)
        password_validation.validate_password(password_confirm)

        return data

    def create(self, data):
        """"""
        data.pop('password_confirm')
        user = User.objects.create_user(**data)
        return user    
