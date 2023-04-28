from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from movie.api.serializers import WatchListSerializer, StreamPlatformSerializer
from movie.models import WatchList, StreamPlatform
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import firebase_admin
from firebase_admin import credentials, messaging
import os
import json

class GetAllStreamPlatformAV(APIView):
    def get(self, request):
        platform = StreamPlatform.objects.filter(active=True).order_by('create_date')[::-1]
        serializer = StreamPlatformSerializer(
            platform, many=True, context={'request': request})
        return Response(serializer.data)
        
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
    permission_classes = [IsAdminUser]
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
            print('serial', serializer.data)
            if(serializer.data['titleNoti'] and serializer.data['summaryNoti']):
                with open('movie/api/cert.json') as file:
                    data = json.load(file)
                creds = credentials.Certificate(data)
                
                firebase_admin.initialize_app(creds)
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
                print('Successfully sent message:  ', res)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
                            
        serializer = StreamPlatformSerializer(
            platform, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        ischecked = request.data['ischecked']
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if (ischecked == 'true'):
                with open('movie/api/cert.json') as file:
                    data = json.load(file)
                creds = credentials.Certificate(data)
                
                firebase_admin.initialize_app(creds)
                movieId = {
                    "id": str(serializer.data['id'])
                }
                message = messaging.Message(
                    notification= messaging.Notification(title=serializer.data['titleNoti'], body=serializer.data['summaryNoti']),
                    topic="demo",
                    data=movieId
                )
                res = messaging.send(message)
                print('Successfully sent message:  ', res)
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
    permission_classes = [IsAdminUser]
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
    permission_classes = [IsAdminUser]
    def get(self, request, pk):
        watchList = WatchList.objects.filter(platform=pk)
        serializer = WatchListSerializer(
            watchList, many=True, context={'request': request})
        return Response(serializer.data)

class WatchListDetailAV(APIView):
    permission_classes = [IsAdminUser]
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
