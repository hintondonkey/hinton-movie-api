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
from hintonmovie.permissions import *


class NotificationEventListAPIView(ListAPIView):
    """
    An endpoint for the client to get all Notification for event.
    """

    permission_classes = (IsBusinessUserOrReadOnly, )
    serializer_class = NotificationSerializer

    def get_queryset(self):
        query = None
        stream_platform_id = self.kwargs.get('stream_platform_id', None)
        if stream_platform_id:
            query = Notification.objects.filter(stream_platform_id=stream_platform_id).order_by('-status', '-create_date')
        return query
    

class NotificationCreateAPIView(CreateAPIView):
    """
    An endpoint for the client to create a new Notification and get Notification list.
    """
    queryset = Notification.objects.all()
    permission_classes = (IsBusinessUserOrReadOnly, )
    serializer_class = NotificationSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
        except Exception as e:
            print(e)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)
    

class NotificationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Get, Update, Delete Notification
    """

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsBusinessUserOrReadOnly, )

    def get_object(self):
        pk = self.kwargs["pk"]
        return get_object_or_404(IsBusinessUserOrReadOnly, id=pk)
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
    