from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins
from django.db.models import Q
from django.shortcuts import get_object_or_404

from lookup.models import Category
from lookup.api.serializers import CategorySerializer
from ..api.serializers import SubCategorySerializer, BrokerServiceSerializer
from ..models import *
from hintonmovie.globals import AccountTypeEnum
from hintonmovie.permissions import IsBusinessAdminOrReadOnly, IsSupervisorOrReadOnly, IsMasterAdminOrReadOnly, IsEditorOrReadOnly, IsBusinessEditorOrReadOnly



class SubCategoryListAPIView(ListAPIView):
    """
    An endpoint for the client to get sub category list.
    """

    permission_classes = (AllowAny, )
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return SubCategory.objects.all()

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = SubCategorySerializer(queryset, many=True)
        return Response(serializer.data)
    

class SubCategoryListCategoryAPIView(ListAPIView):
    """
    An endpoint for the client to get sub category list from category.
    """

    permission_classes = (AllowAny, )
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return SubCategory.objects.filter(category_id=self.args['category_id'])

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = SubCategorySerializer(queryset, many=True)
        return Response(serializer.data)
    
    
class SubCategoryAPIView(ListCreateAPIView):
    """
    An endpoint for the client to create a new syv Category and get sub category list.
    """

    permission_classes = (IsSupervisorOrReadOnly, IsBusinessAdminOrReadOnly, )
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
        broker_id = request.user.profile.broker_id
        created_user_id = request.user.id
        try:
            serializer = self.get_serializer(data=request.data)
        except Exception as e:
            print(e)
        
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.save(broker_id=broker_id, created_user_id=created_user_id)
        return Response(SubCategorySerializer(serializer_data).data, status=status.HTTP_201_CREATED)
    

class SubCategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Get, Update, Delete Category
    """

    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = (IsSupervisorOrReadOnly, IsBusinessAdminOrReadOnly, )

    def get_object(self):
        pk = self.kwargs["pk"]
        return get_object_or_404(SubCategory, id=pk)
    

class BrokerServiceListAPIView(ListAPIView):
    """
    An endpoint for the client to get broker service list.
    """
    permission_classes = (IsMasterAdminOrReadOnly, IsEditorOrReadOnly, )
    serializer_class = BrokerServiceSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        broker_id = self.kwargs["broker_id"]
        return BrokerService.objects.filter(broker_id=broker_id)
    

class BrokerServiceAPIView(RetrieveUpdateAPIView):
    """
    Get, Update Broker service
    """

    queryset = BrokerService.objects.all()
    serializer_class = BrokerServiceSerializer
    permission_classes = (IsMasterAdminOrReadOnly, IsEditorOrReadOnly, )

    def get_object(self):
        pk = self.kwargs["pk"]
        return get_object_or_404(BrokerService, id=pk)


class CategoryBrokerListAPIView(ListAPIView):
    """
    An endpoint for the client to get category list of broker.
    """
    permission_classes = (AllowAny, )
    serializer_class = CategorySerializer

    def get_queryset(self):
        category_id_list = BrokerService.objects.filter(broker_id=self.kwargs['broker_id'], is_active=True).values_list('category_id')
        return Category.objects.filter(id__in=category_id_list)

    