from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins
from django.db.models import Q
from django.shortcuts import get_object_or_404

from ..api.serializers import *
from ..models import *
from services.models import BrokerService
from hintonmovie.globals import *
from hintonmovie.permissions import IsBusinessAdminOrReadOnly, IsSupervisorOrReadOnly, IsMasterAdminOrReadOnly, IsEditorOrReadOnly, IsBusinessEditorOrReadOnly


class NewsListAPIView(ListAPIView):
    """
    An endpoint for the client to get all News.
    """

    permission_classes = (AllowAny, )
    serializer_class = NewsSerializer

    def get_queryset(self):
        query = None
        broker_id = self.kwargs.get('broker_id', None)
        category_id = self.kwargs.get('category_id', None)
        current_date, current_time = get_current_date_time()
        user = self.request.user
        if broker_id and category_id:
            category_id_list = BrokerService.objects.filter(broker_id=broker_id, category_id=category_id, is_active=True).values_list('category_id', flat=True)
            query = News.objects.filter(category_id__in=category_id_list, broker_id=broker_id).order_by('-active', '-create_date')
            if not user:
                query = News.objects.filter(active=True, category_id__in=category_id_list, broker_id=broker_id).filter(Q(post_date__lt=current_date) | (Q(post_date=current_date) & Q(post_time__lte=current_time))).order_by('-create_date')
        return query
    

class NewsCategoryBrokerSubCategoryListAPIView(ListAPIView):
    """
    An endpoint for the client to get News list of broker.
    """
    permission_classes = (AllowAny, )
    serializer_class = NewsSerializer

    def get_queryset(self):
        query = None
        broker_id = self.kwargs.get('broker_id', None)
        category_id = self.kwargs.get('category_id', None)
        subcategory_id = self.kwargs.get('subcategory_id', None)
        current_date, current_time = get_current_date_time()
        user = self.request.user
        if broker_id and category_id:
            category_id_list = BrokerService.objects.filter(broker_id=broker_id, category_id=category_id, is_active=True).values_list('category_id', flat=True)
            if subcategory_id:
                query = News.objects.filter(category_id__in=category_id_list, broker_id=broker_id, subcategory_id=subcategory_id).order_by('-active', '-create_date')
            else:
                query = News.objects.filter(category_id__in=category_id_list, broker_id=broker_id).order_by('-active', '-create_date')
            if not user and query:
                query = query.filter(Q(active=True) & Q(post_date__lt=current_date) | (Q(post_date=current_date) & Q(post_time__lte=current_time))).order_by('-create_date')
        return query
    

class NewsBrokerListAPIView(ListAPIView):
    """
    An endpoint for the client to get StreamPlatform list of broker.
    """
    permission_classes = (AllowAny, )
    serializer_class = NewsSerializer

    def get_queryset(self):
        current_date, current_time = get_current_date_time()
        user = self.request.user
        broker_id = self.kwargs['broker_id']
        category_id_list = BrokerService.objects.filter(broker_id=broker_id, is_active=True).values_list('category_id', flat=True)
        query = News.objects.filter(category_id__in=category_id_list, broker_id=broker_id).order_by('-active', '-create_date')
        if not user:
            query = News.objects.filter(active=True, category_id__in=category_id_list, broker_id=broker_id).filter(Q(post_date__lt=current_date) | (Q(post_date=current_date) & Q(post_time__lte=current_time))).order_by('-create_date')
        return query
    

class NewsAPIView(RetrieveAPIView):
    """
    Get news broker detail
    """

    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (AllowAny, )

    def get_object(self):
        pk = self.kwargs["pk"]
        broker_id = self.kwargs["broker_id"]
        return get_object_or_404(News, id=pk, broker_id=broker_id)
    

class NewsCreateAPIView(CreateAPIView):
    """
    An endpoint for the client to create a new News and get News list.
    """

    permission_classes = (IsSupervisorOrReadOnly, IsEditorOrReadOnly, IsMasterAdminOrReadOnly, IsBusinessAdminOrReadOnly, IsBusinessEditorOrReadOnly, )
    serializer_class = NewsSerializer

    def get_queryset(self):
        user = self.request.user
        query = None
        if user.profile and user.profile.account_type and user.profile.account_type.name in [AccountTypeEnum.BUSINESS_ADMIN.value, AccountTypeEnum.SUPERVISOR.value, AccountTypeEnum.BUSINESS_EDITOR.value] and user.profile.broker and not user.profile.broker.is_network:
            query = News.objects.filter(user__profile__broker=user.profile.broker)
        else:
            query = News.objects.all()
        return query
    
    def get_image_serializer(*args, **kwargs):
        # you can have some logic here...
        return MultipleImage(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
        except Exception as e:
            print(e)
        
        serializer.is_valid(raise_exception=True)
        news = serializer.save()
        image_list = request.data.get('news_image', None)
        if image_list:
            image_serializer = self.get_image_serializer(data=image_list, many=True)
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save()
        else:
            response = {
                'status': 'failed',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Missing news image!',
                'data': []
            }
            return Response(response)
        
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)
    

class NewsRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Get, Update, Delete News
    """

    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (IsSupervisorOrReadOnly, IsEditorOrReadOnly, IsMasterAdminOrReadOnly, IsBusinessAdminOrReadOnly, IsBusinessEditorOrReadOnly, )

    def get_object(self):
        pk = self.kwargs["pk"]
        return get_object_or_404(News, id=pk)
    
    def get_image_serializer(*args, **kwargs):
        # you can have some logic here...
        return MultipleImage(*args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            
            image_list = request.data.get('event_image', None)
            if image_list:
                image_serializer = self.get_image_serializer(data=image_list, many=True)
                if not image_serializer.is_valid():
                    return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            self.object.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'News updated successfully',
                'data': []
            }

            return Response(response)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    