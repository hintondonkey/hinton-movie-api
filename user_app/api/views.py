from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListCreateAPIView, ListAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework import mixins
from django.db.models import Q
from django.shortcuts import get_object_or_404

from user_app.api.serializers import RegistrationSerializer, SubUserSerializer, ProfileSerializer, AccountTypeSerializer, ChangePasswordSerializer, UserSerializer
from ..api import serializers
from ..models import *
from hintonmovie.globals import AccountTypeEnum
from hintonmovie.permissions import IsSupervisorOrReadOnly, IsBusinessAdminOrReadOnly, IsMasterAdminOrReadOnly


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
    serializer_class = SubUserSerializer

    def get_queryset(self):
        user = self.request.user
        
        query = None
        if user.profile:
            if user.profile.is_super_admin and user.profile.broker and user.profile.broker.is_network:
                
                query = Profile.objects.filter(account_type__name__in=[AccountTypeEnum.BUSINESS_ADMIN.value, AccountTypeEnum.EDITOR.value])
            if user.profile.is_super_admin and user.profile.broker and not user.profile.broker.is_network:
                query = Profile.objects.filter(broker=user.profile.broker) # exclude(Q(id=user.id) | (Q(profile__broker__isnull=True) & Q(profile__account_type=AccountTypeEnum.EDITOR.value)))
            if query and query.exists():
                query = query.exclude(user=user).exclude(account_type__isnull=True)
        return query

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
        except Exception as e:
            print(e)
        
        serializer.is_valid(raise_exception=True)
        user = serializer.save(request.data)
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProfileSerializer
        else:
            return SubUserSerializer
    

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
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(token=refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user information
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    

class SubUserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Get, Update, Delete User
    """

    queryset = User.objects.all()
    serializer_class = SubUserSerializer
    permission_classes = (IsSupervisorOrReadOnly, IsBusinessAdminOrReadOnly, IsMasterAdminOrReadOnly, )

    def get_object(self):
        pk = self.kwargs["pk"]
        return get_object_or_404(User, id=pk)
    
    def patch(self, request, pk):
        user = self.get_object()
        serializer = self.get_serializer(instance=user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.update(user, request.data)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user profile
    """

    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileAvatarSerializer
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


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AccountTypeAPIView(ListAPIView):
    """
    Get, Account Type list
    """

    serializer_class = AccountTypeSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        user = self.request.user
        query = None
        if user.profile:
            if user.profile.is_super_admin and user.profile.broker and user.profile.broker.is_network:
                query = AccountType.objects.all().exclude(name__in=[AccountTypeEnum.MASTER_ADMIN.value, AccountTypeEnum.BUSINESS_EDITOR.value, AccountTypeEnum.SUPERVISOR.value, AccountTypeEnum.END_USER.value])
            if user.profile.is_super_admin and user.profile.broker and not user.profile.broker.is_network:
                query = AccountType.objects.filter(name__in=[AccountTypeEnum.EDITOR.value, AccountTypeEnum.SUPERVISOR.value])
        return query

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = AccountTypeSerializer(queryset, many=True)
        return Response(serializer.data)
    
