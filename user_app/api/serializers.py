from ..models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class RegistrationSerializer (serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password' : {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
    
        if password != password2:
            raise serializers.ValidationError({'error': 'P2 should be same!'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':'Email already exists!'})

        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()

        return account


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize User model.
    """
    class Meta:
        model = User
        fields = ("id", "username", "email")


class UserRegisterationSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize registration requests and create a new user.
    """
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SubUserListSerializer(serializers.ModelSerializer):
    account_type = serializers.PrimaryKeyRelatedField(queryset=AccountType.objects.all(), required=False, allow_null=True)
    current_user_id = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "account_type")
        extra_kwargs = {"password": {"write_only": True}}


class SubUserRegisterationSerializer(SubUserListSerializer):
    """
    Serializer class to serialize registration requests and create a new user.
    """

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with email and password.
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
    

class ProfileSerializer(UserSerializer):
    """
    Serializer class to serialize the user Profile model
    """
    class Meta:
        model = Profile
        fields = "__all__"
        

class ProfileAvatarSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize the avatar
    """

    class Meta:
        model = Profile
        fields = ("avatar",)
