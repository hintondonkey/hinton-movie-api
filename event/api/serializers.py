from ..models import *
from rest_framework import serializers
from user_app.api.serializers import BrokerSerializer
from lookup.api.serializers import CategorySerializer

class SubCategorySerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize SubCategory model for event
    """
    broker = BrokerSerializer(many=False, read_only=True)
    total_event = serializers.SerializerMethodField(source='total_event')

    class Meta:
        model = SubCategory
        fields = "__all__"
        extra_fields = ['total_event']
        

class MultipleImageSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize Image Event model for event
    """

    class Meta:
        model = MultipleImage
        fields = "__all__"


class EventSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class to serialize Event model for event
    """
    event_image = MultipleImageSerializer(many=True, read_only=True)
    broker = BrokerSerializer(many=False, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    
    class Meta:
        model = Event
        fields = "__all__"

