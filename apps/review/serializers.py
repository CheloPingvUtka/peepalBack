from rest_framework import serializers
from .models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    photo_url = serializers.ReadOnlyField()

    class Meta:
        model = Photo
        fields = ['id', 'location', 'review', 'image', 'photo_url']
