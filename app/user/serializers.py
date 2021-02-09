from django.contrib.auth import password_validation, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from main.models import User


def validate_register_user(self, data, usert_type):
    """Generic function for validate by user type"""
    password = data.get('password')
    password_confirm = data.get('password_confirm')
    username = data.get('username')

    if password != password_confirm:
        message = 'Las contraseñas no coinciden.'
        raise serializers.ValidationError(message)
    password_validation.validate_password(password_confirm)

    if User.objects.filter(user_type=usert_type, username=username).exists():
        message = 'El nombre de usuario ya existe.'
        raise serializers.ValidationError(message)

    return data

def create_register_user(self, data, user_type):
    """"""
    data.pop('password_confirm')
    data['user_type'] = user_type
    user = User.objects.create_user(**data)
    return user

def validate_login_user(self, data, user_type):
    """"""
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    message = 'El usuario o contraseña es incorrecto.'

    if not user:    
        raise serializers.ValidationError(message)
    if user.user_type == user_type:
        raise serializers.ValidationError(message)
    data['user'] = user

    return data


class UserSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class PassengerLoginSerializer(serializers.Serializer):
    """"""
    username = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """"""
        user_type = 2
        return validate_login_user(self, data, user_type)

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
        user_type = 2
        return validate_register_user(self, data, user_type)

    def create(self, data):
        """"""
        user_type = 2
        return create_register_user(self, data, user_type)


class DriverLoginSerializer(serializers.Serializer):
    """"""
    username = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """"""
        user_type = 2
        return validate_login_user(self, data, user_type)

    def create(self, data):
        """"""
        token, created = Token.objects.get_or_create(user=data['user'])
        return data['user'], token.key


class DriverRegisterSerializer(serializers.Serializer):
    """"""
    username = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirm = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """"""
        user_type = 3
        return validate_register_user(self, data, user_type)

    def create(self, data):
        """"""
        user_type = 3
        return create_register_user(self, data, user_type)


class AdminLoginSerializer(serializers.Serializer):
    """"""
    username = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """"""
        user_type = 1
        return validate_login_user(self, data, user_type)

    def create(self, data):
        """"""
        token, created = Token.objects.get_or_create(user=data['user'])
        return data['user'], token.key
