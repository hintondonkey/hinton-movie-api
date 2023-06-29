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
from hintonmovie.permissions import IsBusinessAdminOrReadOnly, IsSupervisorOrReadOnly, IsBusinessAdminSupervisorOrReadOnly, IsBusinessUserOrReadOnly, IsMasterAdminOrReadOnly, IsMasterUserOrReadOnly, IsEditorOrReadOnly, IsBusinessEditorOrReadOnly



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
        return SubCategory.objects.filter(category_id=self.kwargs['category_id'])

    # def list(self, request):
    #     # Note the use of `get_queryset()` instead of `self.queryset`
    #     queryset = self.get_queryset()
    #     serializer = SubCategorySerializer(queryset, many=True)
    #     return Response(serializer.data)
    
    
class SubCategoryAPIView(ListCreateAPIView):
    """
    An endpoint for the client to create a new syv Category and get sub category list.
    """

    permission_classes = (IsBusinessAdminSupervisorOrReadOnly, )
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
    permission_classes = (IsBusinessAdminSupervisorOrReadOnly, )

    def get_object(self):
        pk = self.kwargs["pk"]
        return get_object_or_404(SubCategory, id=pk)
    
    def patch(self, request, pk):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.update(obj, request.data)
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class BrokerServiceListAPIView(ListAPIView):
    """
    An endpoint for the client to get broker service list.
    """
    permission_classes = (AllowAny, )
    serializer_class = BrokerServiceSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        broker_id = self.kwargs["broker_id"]
        return BrokerService.objects.filter(broker_id=broker_id)
    

class BrokerServiceListAPIView(ListAPIView):
    """
    An endpoint for the client to get broker service list.
    """
    permission_classes = (IsMasterUserOrReadOnly, )
    serializer_class = BrokerServiceSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        broker_id = self.kwargs["broker_id"]
        return BrokerService.objects.filter(broker_id=broker_id)


class BrokerServiceBAListAPIView(ListAPIView):
    """
    An endpoint for the client to get broker service list.
    """
    permission_classes = (IsBusinessUserOrReadOnly, )
    serializer_class = BrokerServiceSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        broker_id = self.request.user.profile.broker_id
        return BrokerService.objects.filter(broker_id=broker_id, is_active=True)
    

class BrokerServiceAPIView(RetrieveUpdateAPIView):
    """
    Get, Update Broker service
    """
    queryset = BrokerService.objects.all()
    serializer_class = BrokerServiceSerializer
    permission_classes = (IsMasterUserOrReadOnly, )
    model = serializer_class.Meta.model

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
        category_id_list = BrokerService.objects.filter(broker_id=self.kwargs['broker_id'], is_active=True).values_list('category_id', flat=True)
        return Category.objects.filter(id__in=category_id_list)


class SubCategoryBrokerListAPIView(ListAPIView):
    """
    An endpoint for the client to get sub category list of broker.
    """
    permission_classes = (AllowAny, )
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        category_id_list = BrokerService.objects.filter(broker_id=self.kwargs['broker_id'], is_active=True).values_list('category_id', flat=True)
        return SubCategory.objects.filter(category_id__in=category_id_list, broker_id=self.kwargs['broker_id']).distinct('id')
    

class SubCategoryCategoryBrokerListAPIView(ListAPIView):
    """
    An endpoint for the client to get sub category list of broker.
    """
    permission_classes = (AllowAny, )
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        category_id_list = BrokerService.objects.filter(broker_id=self.kwargs['broker_id'], is_active=True).values_list('category_id', flat=True)
        return SubCategory.objects.filter(category_id__in=category_id_list, broker_id=self.kwargs['broker_id']).distinct('id')
    
     