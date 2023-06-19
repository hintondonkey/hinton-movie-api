from ..models import *
from rest_framework import serializers


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize SubCategory model for event
    """

    class Meta:
        model = SubCategory
        fields = "__all__"
        

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
    
    class Meta:
        model = Event
        fields = "__all__"

