from ..models import *
from rest_framework import serializers
from user_app.models import User
from django.contrib.auth import authenticate
from hintonmovie.globals import AccountTypeEnum


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


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize User model.
    """
    class Meta:
        model = User
        fields = ("id", "username", "email")


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
    

class UserRegisterationSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize registration requests and create a new user.
    """
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        

class ProfileAvatarSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize the avatar
    """

    class Meta:
        model = Profile
        fields = ("avatar",)


class AccountTypeSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize AccountType model
    """

    class Meta:
        model = AccountType
        fields = "__all__"


class SubUserSerializer(serializers.ModelSerializer):
    account_type = serializers.CharField(source='profile.account_type.name')

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username", "email", "password", "account_type")
        extra_kwargs = {"password": {"write_only": True}}
        related_fields = ['profile']

    def save(self, data={}):
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
    
    def update(self, instance, validated_data):
        for related_obj_name in self.Meta.related_fields:
            if related_obj_name == "profile":
                attr_name = 'account_type'
                data = validated_data.pop(attr_name)
                related_instance = getattr(instance, related_obj_name)
                
                account_type = AccountType.objects.filter(name=data).first()
                value = None
                if account_type:
                    related_instance.account_type = account_type
                    related_instance.save()
        password = validated_data.get("password", None)
        if password and password != '':
            instance.set_password(validated_data.get("password"))
            current_pass = instance.password
            validated_data['password'] = current_pass
        return super(SubUserSerializer, self).update(instance, validated_data)
    

class BrokerSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize Broker model
    """

    class Meta:
        model = Broker
        fields = "__all__"


class ProfileSerializer(UserSerializer):
    """
    Serializer class to serialize the user Profile model
    """
    user = SubUserSerializer(many=False, read_only=True)
    account_type = AccountTypeSerializer(many=False, read_only=True)
    broker = BrokerSerializer(many=False, read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ('is_super_admin', )




