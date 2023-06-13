from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework import mixins
from django.db.models import Q

from user_app.api.serializers import RegistrationSerializer
from ..api import serializers
from ..models import *
from ...hintonmovie.gobals import AccountTypeEnum


@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email

            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)
    

class UserRegisterationAPIView(GenericAPIView):
    """
    An endpoint for the client to create a new User.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserRegisterationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        data["roles"] = {"current_user_id": user.id, "account_type": user.profile.account_type.name if user.profile and user.profile.account_type else None, "is_super_admin": user.profile.is_super_admin if user.profile else False}
        return Response(data, status=status.HTTP_201_CREATED)
    

class SubUserRegisterationAPIView(ListCreateAPIView):
    """
    An endpoint for the client to create a new User.
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.SubUserRegisterationSerializer

    def get_queryset(self):
        user = self.request.user
        query = None
        
        if user.profile:
            query = User.objects.filter(profile__account_type=AccountTypeEnum.BUSINESS_ADMIN.value)
            if user.profile.is_super_admin:
                query = User.objects.exclude(Q(id=user.id) | (Q(profile__broker__isnull=True) & Q(profile__account_type=AccountTypeEnum.EDITOR.value)))

        return query

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.SubUserListSerializer
        else:
            return serializers.SubUserRegisterationSerializer
    

class UserLoginAPIView(GenericAPIView):
    """
    An endpoint to authenticate existing users using their email and password.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = serializers.UserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        data["roles"] = {"current_user_id": user.id, "account_type": user.profile.account_type.name if user.profile and user.profile.account_type else None, "is_super_admin": user.profile.is_super_admin if user.profile else False}
        return Response(data, status=status.HTTP_200_OK)
    

class UserLogoutAPIView(GenericAPIView):
    """
    An endpoint to logout users.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(token=refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
    # def post(self, request, *args, **kwargs):
    #     if self.request.data.get('all'):
    #         token: OutstandingToken
    #         for token in OutstandingToken.objects.filter(user=request.user):
    #             _, _ = BlacklistedToken.objects.get_or_create(token=token)
    #         return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
    #     refresh_token = self.request.data.get('refresh_token')
    #     token = RefreshToken(token=refresh_token)
    #     token.blacklist()
    #     return Response({"status": "OK, goodbye"})


class UserAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user information
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user
    

class UserProfileAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user profile
    """

    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile


class UserAvatarAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user avatar
    """

    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileAvatarSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile
