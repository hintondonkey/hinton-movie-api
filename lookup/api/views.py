from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework import mixins
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from ..api.serializers import CategorySerializer
from ..models import *
from hintonmovie.globals import AccountTypeEnum
from hintonmovie.permissions import IsMasterAdminOrReadOnly



class CategoryListAPIView(ListAPIView):
    """
    An endpoint for the client to get category list.
    """

    permission_classes = (AllowAny, )
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
    

class CategoryListCreateAPIView(ListCreateAPIView):
    """
    An endpoint for the client to create a new Category.
    """

    permission_classes = (IsMasterAdminOrReadOnly, )
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        return Category.objects.all()

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        category_name = str(request.POST['name']).strip() if request.POST['name'] else None
        if Category.objects.filter(name=category_name).exists():
            raise ValidationError(("This category already existed!"))
        else:
            return super().create(request, *args, **kwargs)
        

class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Get, Update, Delete Category
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsMasterAdminOrReadOnly,)

    def get_object(self):
        pk = self.kwargs["pk"]
        return get_object_or_404(Category, id=pk)
