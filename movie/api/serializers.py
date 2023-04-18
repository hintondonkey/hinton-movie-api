from rest_framework import serializers
from movie.models import WatchList
from movie.models import StreamPlatform

class WatchListSerializer(serializers.ModelSerializer):
    class  Meta:
        model = WatchList
        fields = '__all__'

class StreamPlatformSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    watchlist = WatchListSerializer(many=True, read_only=True)

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

# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short!")
# class StreamPlatformSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(validators=[name_length])
#     description = serializers.Charfield()
#     image = serializers.Charfield()
#     show_date = serializers.DateField()
#     time_show_date = serializers.TimeField()
#     close_date = serializers.DateField()
#     time_close_date = serializers.TimeField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return StreamPlatform.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.image = validated_data.get ('image', instance.image)
#         instance.show_date = validated_data.get('show_date', instance.show_date)
#         instance.time_show_date = validated_data.get('time_show_date', instance.time_show_date)
#         instance.close_date = validated_data.get('close_date', instance.close_date)
#         instance.time_close_date = validated_data.get('time_close_date', instance.time_close_date)
#         instance.active = validated_data.get ('active', instance.active)
#         instance.save()
#         return instance
#     def validate(self, data):
#         if data['title'] == data['description']:
#             raise serializers.ValidationError("Title and Description should be different!")
#         else:
#             return data