from rest_framework import serializers
from .models import Location, LocationCategory, LocationChange, Filter, LocationFilter
from apps.user.models import User  # проверь, что путь правильный


class LocationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCategory
        fields = ['id', 'category_name']

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class LocationSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField()
    filters = serializers.PrimaryKeyRelatedField(queryset=Filter.objects.all(), many=True, write_only=True)

    category = LocationCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=LocationCategory.objects.all(), write_only=True)

    user = UserShortSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Location
        fields = [
            'id', 'address', 'description', 'status',
            'latitude', 'longitude', 'created_at', 'updated_at',
            'city_name',
            'category', 'category_id',
            'user', 'user_id',
            'filters'
        ]

    def create(self, validated_data):
        # Извлекаем filters, category_id и user_id
        filters = validated_data.pop('filters', [])
        category = validated_data.pop('category_id')
        user = validated_data.pop('user_id')

        location = Location.objects.create(
            category=category,
            user=user,
            **validated_data
        )

        for f in filters:
            LocationFilter.objects.create(location=location, filter=f)

        return location

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