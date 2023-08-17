from ..models import *
from rest_framework import serializers
from user_app.api.serializers import BrokerSerializer
from lookup.api.serializers import CategorySerializer
        

class MultipleImageSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize Image News model for event
    """

    class Meta:
        model = MultipleImage
        fields = "__all__"


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class to serialize News model for news
    """
    news_image = MultipleImageSerializer(many=True, read_only=True)
    broker = BrokerSerializer(many=False, read_only=True)
    category_name = serializers.CharField(source='category.name', required=False, allow_null=True, allow_blank=True)
    subcategory_name = serializers.CharField(source='subcategory.name', required=False, allow_null=True, allow_blank=True)
    
    class Meta:
        model = News
        fields = "__all__"
        extra_fields = ['category_name', 'subcategory_name']

