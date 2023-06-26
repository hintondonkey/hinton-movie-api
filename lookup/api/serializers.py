from ..models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize Category model
    """
    total_event = serializers.SerializerMethodField(source='get_total_event')

    class Meta:
        model = Category
        fields = "__all__"
        extra_fields = ['total_event']

    def get_total_event(self, caterory):
        num = 0
        if caterory:
            num = caterory.total_stream_platform
        return num
    
        

