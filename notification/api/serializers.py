from ..models import *
from rest_framework import serializers
        

class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class to serialize Notification model for Notification
    """
    
    class Meta:
        model = Notification
        fields = "__all__"

