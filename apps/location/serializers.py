from rest_framework import serializers
from .models import Location, City, LocationCategory
from apps.user.models import User 

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name', 'latitude', 'longitude']

class LocationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCategory
        fields = ['id', 'category_name']

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class LocationSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), write_only=True)

    category = LocationCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=LocationCategory.objects.all(), write_only=True)

    user = UserShortSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Location
        fields = [
            'id', 'address', 'description', 'status',
            'latitude', 'longitude', 'created_at', 'updated_at',
            'city', 'city_id',
            'category', 'category_id',
            'user', 'user_id',
        ]
