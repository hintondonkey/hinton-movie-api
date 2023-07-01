from rest_framework import serializers
from movie.models import StreamPlatform, WatchList, MultipleImage

from lookup.api.serializers import CategorySerializer
from services.api.serializers import SubCategorySerializer


class WatchListSerializer(serializers.ModelSerializer):
    class  Meta:
        model = WatchList
        fields = '__all__'


class MultipleImageSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize Image Event model for event
    """

    class Meta:
        model = MultipleImage
        fields = "__all__"


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    stream_flatform_image = MultipleImageSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', required=False, allow_null=True, allow_blank=True)
    subcategory_name = serializers.CharField(source='subcategory.name', required=False, allow_null=True, allow_blank=True)

    class  Meta:
        model = StreamPlatform
        fields = '__all__'
        extra_fields = ['category_name', 'subcategory_name']

    def validate(self, data):
        if "title" in data and "description" in data and data['title'] == data['description']:
            raise serializers.ValidationError("Title and Description should be different!")
        else:
            return data
        
    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.validationError("Name is too short!")
        else:
            return value
        
    def update(self):
        return super(StreamPlatform, self).update(self.instance, self.validated_data)
    
    def save(self, **data):
        broker_id = data.get('broker_id', None)
        created_user_id = data.get('created_user_id', None)

        if StreamPlatform.objects.filter(title=self.validated_data['title']).exists():
            raise serializers.ValidationError({'error': 'Stream Platform already exists!'})

        stream_platform = StreamPlatform(**self.validated_data)
        if broker_id:
            stream_platform.broker_id = broker_id
        if created_user_id:
            stream_platform.created_user_id = created_user_id
        stream_platform.save()
        return stream_platform
