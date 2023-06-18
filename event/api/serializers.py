from ..models import *
from rest_framework import serializers


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize SubCategory model for event
    """

    class Meta:
        model = SubCategory
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize Event model for event
    """

    class Meta:
        model = Event
        fields = "__all__"

