from rest_framework import serializers
from .models import Location, City, LocationCategory, LocationChange, Filter, LocationFilter
from apps.user.models import User 

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'  

class LocationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCategory
        fields = '__all__'  

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

class LocationChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationChange
        fields = '__all__' 

class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = '__all__' 

class LocationFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationFilter
        fields = '__all__'  
