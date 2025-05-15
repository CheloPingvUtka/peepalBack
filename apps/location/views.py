from rest_framework.viewsets import ModelViewSet
from .models import Location, LocationCategory
from .serializers import LocationSerializer, LocationCategorySerializer

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationCategoryViewSet(ModelViewSet):
    queryset = LocationCategory.objects.all()
    serializer_class = LocationCategorySerializer
