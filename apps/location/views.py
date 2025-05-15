from rest_framework.viewsets import ModelViewSet
from .models import LocationCategory, Location, LocationChange, Filter, LocationFilter
from .serializers import LocationCategorySerializer, LocationSerializer, LocationChangeSerializer, FilterSerializer, LocationFilterSerializer


class LocationCategoryViewSet(ModelViewSet):
    queryset = LocationCategory.objects.all()
    serializer_class = LocationCategorySerializer

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationChangeViewSet(ModelViewSet):
    queryset = LocationChange.objects.all()
    serializer_class = LocationChangeSerializer

class FilterViewSet(ModelViewSet):
    queryset = Filter.objects.all()
    serializer_class = FilterSerializer

class LocationFilterViewSet(ModelViewSet):
    queryset = LocationFilter.objects.all()
    serializer_class = LocationFilterSerializer