from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import status
from movie.api.serializers import WatchListSerializer, StreamPlatformSerializer, MultipleImageSerializer, StreamPlatformActiveSerializer
from movie.models import WatchList, StreamPlatform, MultipleImage
from services.models import BrokerService
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, CreateAPIView, ListCreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
import firebase_admin
from firebase_admin import credentials, messaging
import os
import json
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import datetime

from hintonmovie.permissions import *

creds = credentials.Certificate("movie/api/cert.json")
firebase_admin.initialize_app(creds)



def get_current_date_time():
    current_date_time = datetime.now()
    return current_date_time.strftime("%Y-%m-%d"), current_date_time.strftime("%H:%M:%S")


def send_notification(topic, data, title, content):
    try:
        if title and content:
            message = messaging.Message(
                notification= messaging.Notification(title=title, 
                                                        body=content),
                topic="demo",
                data=data
            )
            messaging.send(message)
    except Exception as e:
        print("Error while send notification as message: ", e)


class GetAllStreamPlatformAV(APIView):
    def get(self, request):
        platform = StreamPlatform.objects.filter(active=True).order_by('create_date')[::-1]
        serializer = StreamPlatformSerializer(
            platform, many=True, context={'request': request})
        return Response(serializer.data)
        

class StreamPlatformCategoryBrokerListAPIView(ListAPIView):
    """
    An endpoint for the client to get StreamPlatform list of broker.
    """
    permission_classes = (AllowAny, )
    serializer_class = StreamPlatformSerializer

    def get_queryset(self):
        query = None
        broker_id = self.kwargs.get('broker_id', None)
        category_id = self.kwargs.get('category_id', None)
        current_date, current_time = get_current_date_time()
        user = self.request.user
        if broker_id and category_id:
            category_id_list = BrokerService.objects.filter(broker_id=broker_id, category_id=category_id, is_active=True).values_list('category_id', flat=True)
            query = StreamPlatform.objects.filter(category_id__in=category_id_list, broker_id=broker_id).order_by('-active', 'create_date')
            if not user:
                query = StreamPlatform.objects.filter(active=True, category_id__in=category_id_list, broker_id=broker_id).filter(Q(post_date__lt=current_date) | (Q(post_date=current_date) & Q(post_time__lte=current_time))).order_by('create_date')
        return query
    

class StreamPlatformCategoryBrokerSubCategoryListAPIView(ListAPIView):
    """
    An endpoint for the client to get StreamPlatform list of broker.
    """
    permission_classes = (AllowAny, )
    serializer_class = StreamPlatformSerializer

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
                query = StreamPlatform.objects.filter(category_id__in=category_id_list, broker_id=broker_id, subcategory_id=subcategory_id).order_by('-active', 'create_date')
            else:
                query = StreamPlatform.objects.filter(category_id__in=category_id_list, broker_id=broker_id).order_by('-active', 'create_date')
            if not user and query:
                query = query.filter(Q(active=True) & Q(post_date__lt=current_date) | (Q(post_date=current_date) & Q(post_time__lte=current_time))).order_by('create_date')
        return query
    

class StreamPlatformBrokerListAPIView(ListAPIView):
    """
    An endpoint for the client to get StreamPlatform list of broker.
    """
    permission_classes = (AllowAny, )
    serializer_class = StreamPlatformSerializer

    def get_queryset(self):
        current_date, current_time = get_current_date_time()
        user = self.request.user
        broker_id = self.kwargs['broker_id']
        category_id_list = BrokerService.objects.filter(broker_id=broker_id, is_active=True).values_list('category_id', flat=True)
        query = StreamPlatform.objects.filter(category_id__in=category_id_list, broker_id=broker_id).order_by('-active', 'create_date')
        if not user:
            query = StreamPlatform.objects.filter(active=True, category_id__in=category_id_list, broker_id=broker_id).filter(Q(post_date__lt=current_date) | (Q(post_date=current_date) & Q(post_time__lte=current_time))).order_by('create_date')
        return query
    

class StreamPlatformAPIView(RetrieveAPIView):
    """
    Get stream platform broker detail
    """

    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = (AllowAny, )

    def get_object(self):
        pk = self.kwargs["pk"]
        broker_id = self.kwargs["broker_id"]
        return get_object_or_404(StreamPlatform, id=pk, broker_id=broker_id)
    

class StreamPlatformCreateAPIView(CreateAPIView):
    """
    create stream platform
    """

    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = (IsBusinessAdminSupervisorOrReadOnly, )

    def post(self, request, *args, **kwargs):
        broker_id = request.user.profile.broker_id
        created_user_id = request.user.id
        
        serializer = self.get_serializer(data=request.data)

        watchlist = request.data.get('watchlist')
        stream_platform_image = request.data.get('stream_platform_image')
        stream_platform_id = None
        if serializer.is_valid(raise_exception=True):
            stream_platform = serializer.save(broker_id=broker_id, created_user_id=created_user_id)
            stream_platform_id = stream_platform.id

            if stream_platform_id and watchlist:
                for watch in list(watchlist):
                    watch['platform'] = stream_platform_id
                    watchlist_serializer = WatchListSerializer(data=watch)
                    if watchlist_serializer.is_valid():
                        watchlist_serializer.save()
                    else:
                        return Response(watchlist_serializer.errors)
    
            if stream_platform_id and stream_platform_image:
                for image in list(stream_platform_image):
                    image['stream_platform'] = stream_platform_id
                    multiple_image_serializer = MultipleImageSerializer(data=image)
                    if multiple_image_serializer.is_valid():
                        multiple_image_serializer.save()
                    else:
                        return Response(multiple_image_serializer.errors)
            
            send_notification("demo", stream_platform_id, serializer.data['titleNoti'], serializer.data['summaryNoti'])
        stream_flatform = StreamPlatform.objects.filter(id=stream_platform_id).first()
        return Response(StreamPlatformSerializer(stream_flatform).data, status=status.HTTP_201_CREATED)
    
    
class StreamPlatformRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Get, Update, Delete Stream Platform
    """

    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = (IsBusinessAdminSupervisorOrReadOnly, )

    def get_object(self):
        pk = self.kwargs["pk"]
        return get_object_or_404(StreamPlatform, id=pk)
    
    def put(self, request, pk):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj, data=request.data, partial=True)
        is_checked = request.data['is_notification']
        stream_platform_image = request.data.get('stream_platform_image')
        
        if serializer.is_valid(raise_exception=True):
            serializer.update(obj)
            current_id = request.data.get('id')
            if is_checked:
                stream_platform_id = {
                    "id": str(current_id)
                }
                send_notification("demo", stream_platform_id, serializer.data['titleNoti'], serializer.data['summaryNoti'])

            stream_platform_id = current_id
            MultipleImage.objects.filter(stream_platform_id=int(stream_platform_id)).delete()
            if stream_platform_image:
                for image in stream_platform_image:
                    image['stream_platform'] = stream_platform_id
                    multiple_image_serializer = MultipleImageSerializer(data=image)
                    if multiple_image_serializer.is_valid():
                        multiple_image_serializer.save()
                    else:
                        return Response(multiple_image_serializer.errors)
                    
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
class GetStreamPlatformDetailAV(APIView):
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
                             
        serializer = StreamPlatformSerializer(
            platform, context={'request': request})
        return Response(serializer.data)
    

class StreamPlatformAV(APIView):
    permission_classes = [IsBusinessAdminSupervisorOrReadOnly]
    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(
            platform, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        watchlist = []
        for i in range(100):
            print('i watchlist', i)
            if request.data.get('watchlist['+ str(i) +'][website]'):
                watchlist_request = {
                    "date_picker": request.data.get('watchlist['+ str(i) +'][date_picker]'),
                    "time_show_date": request.data.get('watchlist['+ str(i) +'][time_show_date]'),
                    "price": request.data.get('watchlist['+ str(i) +'][price]'),
                    "website": request.data.get('watchlist['+ str(i) +'][website]'),
                    "active": True
                }
                watchlist.append(watchlist_request)
            else:
                break
        request.data['active'] = True
        serializer = StreamPlatformSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            movieId = serializer.data.get('id')
            if(movieId and watchlist):
                for watch in watchlist:
                    watch['platform'] = movieId
                    watchListSerializer = WatchListSerializer(data=watch)
                    if watchListSerializer.is_valid():
                        watchListSerializer.save()
                        serializer.data['watchlist'].append(watchListSerializer.data)

                    else:
                        return Response(watchListSerializer.errors)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StreamPlatPostformAV(APIView):

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        watchlist = request.data.get('watchlist')
        if not serializer.is_valid():
            print(serializer.errors)
        if serializer.is_valid():
            serializer.save()
            movieId = serializer.data.get('id')
            if(movieId and watchlist):
                for watch in watchlist:
                    watch['platform'] = movieId
                    watchListSerializer = WatchListSerializer(data=watch)
                    if watchListSerializer.is_valid():
                        watchListSerializer.save()
                        serializer.data['watchlist'].append(watchListSerializer.data)
                    else:
                        return Response(watchListSerializer.errors)
            print("============================================================================")
            print('serial', serializer.data)
            print("============================================================================")
            if(serializer.data['titleNoti'] and serializer.data['summaryNoti']):
                # with open('movie/api/cert.json') as file:
                #     data = json.load(file)
                # creds = credentials.Certificate(data)
                
                # firebase_admin.initialize_app(creds)
                movieId = {
                    "id": str(serializer.data['id'])
                }
                message = messaging.Message(
                    notification= messaging.Notification(title=serializer.data['titleNoti'], 
                                                         body=serializer.data['summaryNoti']),
                    topic="demo",
                    data=movieId
                )
                res = messaging.send(message)
                print("============================================================================")
                print('Successfully sent message:  ', res)
                print("============================================================================")
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class StreamPlatformDetailAV(APIView):
    permission_classes = [IsBusinessAdminSupervisorOrReadOnly]
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
                            
        serializer = StreamPlatformSerializer(
            platform, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        print('Successfully sent message: ')
        ischecked = request.data['ischecked']
        print(ischecked)
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if (ischecked==True):
                # with open('movie/api/cert.json') as file:
                #     data = json.load(file)
                # creds = credentials.Certificate(data)
                
                # firebase_admin.initialize_app(creds)
                movieId = {
                    "id": str(serializer.data['id'])
                }
                message = messaging.Message(
                    notification= messaging.Notification(title=serializer.data['titleNoti'], body=serializer.data['summaryNoti']),
                    topic="demo",
                    data=movieId
                )
                res = messaging.send(message)
                print("============================================================================")
                print('Successfully sent message:  ', res)
                print("============================================================================")
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platformtitle = StreamPlatform.objects.get(pk=pk).title

        platform.delete()
        return Response(
            {"Success": "Delete " + platformtitle + " successfully!"}
        )
    

class WatchListAV(APIView):
    permission_classes = [IsBusinessAdminSupervisorOrReadOnly]
    def get(self, request):
        watchList = WatchList.objects.all()
        serializer = WatchListSerializer(
            watchList, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print('response watch list', serializer.data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

class GetWatchListByPlatformIdAV(APIView):
    permission_classes = [IsBusinessAdminSupervisorOrReadOnly]
    def get(self, request, pk):
        watchList = WatchList.objects.filter(platform=pk)
        serializer = WatchListSerializer(
            watchList, many=True, context={'request': request})
        return Response(serializer.data)


class WatchListDetailAV(APIView):
    permission_classes = [IsBusinessAdminSupervisorOrReadOnly]
    def get(self, request, pk):
        try:
            watchList = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
                             
        serializer = WatchListSerializer(
            watchList, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        watchList = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(watchList, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        watchList = WatchList.objects.get(pk=pk)
        watchList.delete()
        return Response(
            {"Success": "Delete watch list successfully!"}
        )


class UpdateNotificationAV(APIView):
    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        print("data: ", platform)
        noti = request.data['notification']
        if noti:
            print("noti: ", noti)
            serializer = StreamPlatformSerializer(platform, data=request.data)
            if serializer.is_valid():
                serializer.save()
                noti = StreamPlatform.objects.get(pk=pk)
                if noti.notification:
                    print("check noti: ", noti.notification)
                    # GetNotification.get(self,context=request,pk=noti.id)

                else:
                    print("noti is not added")
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            pass
            
class GetNotification(APIView):
    def get(self, request):
        try:
            noti = StreamPlatform.objects.filter(active_noti=True, active=True)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
                             
        serializer = StreamPlatformSerializer(
            noti, many=True, context={'request': request})
        print("check notioiiii: ", Response(serializer.data))
        return Response(serializer.data)
    

class NumberOfConnectionMovieUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = StreamPlatformSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    

class StreamPlatformActiveUpdateAPIView(UpdateAPIView):
    permission_classes = [IsBusinessAdminSupervisorOrReadOnly]
    serializer_class = StreamPlatformActiveSerializer

    def get_object(self):
        pk = self.kwargs["pk"]
        return get_object_or_404(StreamPlatform, id=pk)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
