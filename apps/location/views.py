from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from django.db.models import Count
from .models import LocationCategory, Location, LocationChange, Filter, LocationFilter
from .serializers import LocationCategorySerializer, LocationSerializer, LocationChangeSerializer, FilterSerializer, LocationFilterSerializer


class LocationCategoryViewSet(ModelViewSet):
    queryset = LocationCategory.objects.all()
    serializer_class = LocationCategorySerializer

class LocationViewSet(ModelViewSet):
    serializer_class = LocationSerializer

    def get_queryset(self):
        queryset = Location.objects.all()
        category = self.request.query_params.get('category')
        filters = self.request.query_params.getlist('filters')

        if category:
            queryset = queryset.filter(category_id=category)

        if filters:
            # Преобразуем в числа (на всякий случай)
            filter_ids = list(map(int, filters))

            # Находим локации, у которых есть все нужные фильтры
            queryset = queryset.annotate(
                matched_filters=Count('locationfilter', filter=Q(locationfilter__filter_id__in=filter_ids), distinct=True)
            ).filter(matched_filters=len(filter_ids))

        return queryset.distinct()

class LocationChangeViewSet(ModelViewSet):
    queryset = LocationChange.objects.all()
    serializer_class = LocationChangeSerializer

class FilterViewSet(ModelViewSet):
    queryset = Filter.objects.all()
    serializer_class = FilterSerializer
    

class LocationFilterViewSet(ModelViewSet):
    queryset = LocationFilter.objects.all()
    serializer_class = LocationFilterSerializer