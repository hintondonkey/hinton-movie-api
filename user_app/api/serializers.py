from ..models import *
from rest_framework import serializers
from user_app.models import User
from django.contrib.auth import authenticate


class RegistrationSerializer (serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
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
        fields = ("id", "first_name", "last_name", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}, "password2": {"write_only": True}}

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


class SubUserSerializer(serializers.ModelSerializer):
    # account_type = serializers.SerializerMethodField()
    # current_user_id = serializers.SerializerMethodField()
    # profile = ProfileSerializer(many=False)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}
    
    def save(self, data):
        password = self.validated_data['password']
        password2 = data.get('password2', '')
        account_type = data.get('account_type', '')
        current_user_id = data.get('current_user_id', '')

        if password != password2:
            raise serializers.ValidationError({'error': 'P2 should be same!'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})
    
        account = User(email=self.validated_data['email'], username=self.validated_data['username'], first_name=self.validated_data['first_name'], last_name=self.validated_data['last_name'])
        account.set_password(password)
        account.account_type = account_type
        account.current_user_id = current_user_id
        account.save()
        return account



# class SubUserRegisterationSerializer(SubUserSerializer):
#     """
#     Serializer class to serialize registration requests and create a new user.
#     """

#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)


class ProfileSerializer(UserSerializer):
    """
    Serializer class to serialize the user Profile model
    """
    user = SubUserSerializer(many=False)

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
