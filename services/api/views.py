from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins
from django.db.models import Q
from django.shortcuts import get_object_or_404

from ..api.serializers import SubCategorySerializer
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
        try:
            serializer = self.get_serializer(data=request.data)
        except Exception as e:
            print(e)
        
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)
    

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
    