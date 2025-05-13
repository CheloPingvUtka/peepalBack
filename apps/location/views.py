from rest_framework.viewsets import ModelViewSet
from .models import Location, City, LocationCategory
from .serializers import LocationSerializer, CitySerializer, LocationCategorySerializer

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class LocationCategoryViewSet(ModelViewSet):
    queryset = LocationCategory.objects.all()
    serializer_class = LocationCategorySerializer
