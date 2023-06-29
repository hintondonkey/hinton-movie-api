from ..models import *
from rest_framework import serializers
from user_app.api.serializers import BrokerSerializer, UserSerializer
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
        extra_kwargs = {
            'name' : {'read_only': True},
            'price' : {'read_only': True}
        }


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize SubCategory model for event
    """
    broker = BrokerSerializer(many=False, read_only=True)
    total_event = serializers.SerializerMethodField(source='get_total_event')
    created_user = UserSerializer(many=False, read_only=True)
    category_name = serializers.CharField(source='category.name', required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = SubCategory
        fields = "__all__"
        extra_fields = ['total_event', 'category_name']
    
    def get_total_event(self, caterory):
        num = 0
        if caterory:
            num = caterory.total_stream_platform
        return num
    
    def get_parent_category_name(self, caterory):
        return caterory.name if caterory else ''
    
    def save(self, **data):
        broker_id = data.get('broker_id', None)
        created_user_id = data.get('created_user_id', None)
        
        if not broker_id or not created_user_id:
            raise serializers.ValidationError({'error': 'Missing required fields!'})

        if SubCategory.objects.filter(name=self.validated_data['name']).exists():
            raise serializers.ValidationError({'error': 'Subcategory already exists!'})

        subcategory = SubCategory(**self.validated_data)
        subcategory.broker_id = broker_id
        subcategory.created_user_id = created_user_id
        subcategory.save()
        return subcategory
    




