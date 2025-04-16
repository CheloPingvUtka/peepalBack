from rest_framework.viewsets import ModelViewSet
from .models import Location, Region, LocationCategory
from .serializers import LocationSerializer, RegionSerializer, LocationCategorySerializer

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class RegionViewSet(ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class LocationCategoryViewSet(ModelViewSet):
    queryset = LocationCategory.objects.all()
    serializer_class = LocationCategorySerializer
