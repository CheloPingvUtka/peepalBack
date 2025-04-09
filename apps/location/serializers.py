from rest_framework import serializers
from .models import (
    Region, LocationCategory, Location,
    LocationChange, Filter, LocationFilter
)

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class LocationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCategory
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

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
