from rest_framework import viewsets
from .models import City, LocationCategory, Location, LocationChange, Filter, LocationFilter
from .serializers import CitySerializer, LocationCategorySerializer, LocationSerializer, LocationChangeSerializer, FilterSerializer, LocationFilterSerializer

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class LocationCategoryViewSet(viewsets.ModelViewSet):
    queryset = LocationCategory.objects.all()
    serializer_class = LocationCategorySerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationChangeViewSet(viewsets.ModelViewSet):
    queryset = LocationChange.objects.all()
    serializer_class = LocationChangeSerializer

class FilterViewSet(viewsets.ModelViewSet):
    queryset = Filter.objects.all()
    serializer_class = FilterSerializer

class LocationFilterViewSet(viewsets.ModelViewSet):
    queryset = LocationFilter.objects.all()
    serializer_class = LocationFilterSerializer
