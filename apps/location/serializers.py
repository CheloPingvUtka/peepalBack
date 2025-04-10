from rest_framework import serializers
from .models import Location, Region, LocationCategory
from apps.user.models import User  # проверь, что путь правильный

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'region_name', 'latitude', 'longitude']

class LocationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCategory
        fields = ['id', 'category_name']

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class LocationSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), write_only=True)

    category = LocationCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=LocationCategory.objects.all(), write_only=True)

    user = UserShortSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Location
        fields = [
            'id', 'address', 'description', 'status',
            'latitude', 'longitude', 'created_at', 'updated_at',
            'region', 'region_id',
            'category', 'category_id',
            'user', 'user_id',
        ]
