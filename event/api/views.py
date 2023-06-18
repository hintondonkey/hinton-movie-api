from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins
from django.db.models import Q

from ..api.serializers import SubCategorySerializer
from ..models import *
from hintonmovie.globals import AccountTypeEnum


class SubCategoryAPIView(ListCreateAPIView):
    """
    An endpoint for the client to create a new Category and get category list.
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        user = self.request.user
        query = None
        if user.profile and user.profile.account_type and user.profile.account_type.name in [AccountTypeEnum.BUSINESS_ADMIN.value, AccountTypeEnum.SUPERVISOR.value] and user.profile.broker and not user.profile.broker.is_network:
            query = SubCategory.objects.filter(broker=user.profile.broker)
        return query

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = SubCategorySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
        except Exception as e:
            print(e)
        
        serializer.is_valid(raise_exception=True)
        subcategory = serializer.save(request.data)
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)
    

class EventAPIView(ListCreateAPIView):
    """
    An endpoint for the client to create a new Event and get Event list.
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        user = self.request.user
        query = None
        if user.profile and user.profile.account_type and user.profile.account_type.name in [AccountTypeEnum.BUSINESS_ADMIN.value, AccountTypeEnum.SUPERVISOR.value] and user.profile.broker and not user.profile.broker.is_network:
            query = SubCategory.objects.filter(broker=user.profile.broker)
        return query

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = SubCategorySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
        except Exception as e:
            print(e)
        
        serializer.is_valid(raise_exception=True)
        subcategory = serializer.save(request.data)
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)