from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from movie.api.serializers import WatchListSerializer, StreamPlatformSerializer
from movie.models import WatchList, StreamPlatform
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

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
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
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
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
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
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
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

    def put (self, request, pk):
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
        
class GetNotification(APIView):
    def get(self, request, pk):
        try:
            notification = StreamPlatform.objects.get(pk=pk).notification
            print("check noti get: ", notification)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
                             
        serializer = StreamPlatformSerializer(
            notification, context={'request': request})
        print("check notioiiii: ", Response(serializer.data))
        return Response(serializer.data)
