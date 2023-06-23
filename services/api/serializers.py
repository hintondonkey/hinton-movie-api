from ..models import *
from rest_framework import serializers
from user_app.api.serializers import BrokerSerializer
from lookup.api.serializers import CategorySerializer


class BrokerServiceSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize BrokerService model
    """
    broker = BrokerSerializer(many=False, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    
    class Meta:
        model = BrokerService
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize SubCategory model for event
    """
    broker = BrokerSerializer(many=False, read_only=True)
    total_event = serializers.SerializerMethodField(source='get_total_event')

    class Meta:
        model = SubCategory
        fields = "__all__"
        extra_fields = ['total_event']
    
    def get_total_event(self, caterory):
        num = 0
        if caterory:
            num = caterory.total_stream_platform
        return num





