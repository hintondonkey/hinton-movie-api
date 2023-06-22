from ..models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize Category model
    """

    class Meta:
        model = Category
        fields = "__all__"

