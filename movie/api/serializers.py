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
    category = CategorySerializer(many=False, read_only=True)
    subcategory = SubCategorySerializer(many=True, read_only=True)

    class  Meta:
        model = StreamPlatform
        fields = '__all__'

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
