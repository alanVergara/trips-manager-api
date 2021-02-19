from django.contrib.auth import password_validation, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from main.models import User


def validate_register_user(self, data, usert_type):
    """Generic function for validate register by user type"""
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
    """Generic function for creating user by user type"""
    data.pop('password_confirm')
    data['user_type'] = user_type
    user = User.objects.create_user(**data)
    return user


def validate_login_user(self, data, user_type):
    """Generic function for validate login by user type"""
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    message = 'El usuario o contraseña es incorrecto.'

    if not user:
        raise serializers.ValidationError(message)
    data['user'] = user

    return data


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User object"""
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'user_type',)
        read_only_fields = ('user_type', 'id',)
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, data):
        """Update a user, setting the password"""
        password = data.pop('password', None)
        user = super().update(instance, data)

        if password:
            user.set_password(password)
            user.save()

        return user


class PassengerLoginSerializer(serializers.Serializer):
    """Serializer for passenger login"""
    username = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Validate login data"""
        user_type = 2
        return validate_login_user(self, data, user_type)

    def create(self, data):
        """Token creation"""
        token, created = Token.objects.get_or_create(user=data['user'])
        return data['user'], token.key


class PassengerRegisterSerializer(serializers.Serializer):
    """Serializer for register passenger"""
    username = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirm = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Validate register passenger"""
        user_type = 2
        return validate_register_user(self, data, user_type)

    def create(self, data):
        """Creation new passenger"""
        user_type = 2
        return create_register_user(self, data, user_type)


class DriverLoginSerializer(serializers.Serializer):
    """Serializer for driver login"""
    username = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Validate login data user"""
        user_type = 3
        return validate_login_user(self, data, user_type)

    def create(self, data):
        """Token creation"""
        token, created = Token.objects.get_or_create(user=data['user'])
        return data['user'], token.key


class DriverRegisterSerializer(serializers.Serializer):
    """Serializer for register driver"""
    username = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirm = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Validate driver register data"""
        user_type = 3
        return validate_register_user(self, data, user_type)

    def create(self, data):
        """Creation new driver"""
        user_type = 3
        return create_register_user(self, data, user_type)


class AdminLoginSerializer(serializers.Serializer):
    """Serializer for admin login"""
    username = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Validate login data"""
        user_type = 1
        return validate_login_user(self, data, user_type)

    def create(self, data):
        """Token creation"""
        token, created = Token.objects.get_or_create(user=data['user'])
        return data['user'], token.key
