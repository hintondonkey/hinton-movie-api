from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListCreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework import mixins
from django.db.models import Q

from ..api.serializers import CategorySerializer
from ..models import *
from hintonmovie.globals import AccountTypeEnum


class CategoryAPIView(ListCreateAPIView):
    """
    An endpoint for the client to create a new Category and get category list.
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user
        query = None
        if user.profile:
            if user.profile.is_super_admin and user.profile.broker and user.profile.broker.is_network:
                query = Category.objects.all()
        return query

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
        except Exception as e:
            print(e)
        
        serializer.is_valid(raise_exception=True)
        category = serializer.save(request.data)
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)