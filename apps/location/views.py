from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from django.db.models import Count
from .models import LocationCategory, Location, LocationChange, Filter, LocationFilter
from .serializers import LocationCategorySerializer, LocationSerializer, LocationChangeSerializer, FilterSerializer, LocationFilterSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class LocationViewSet(ModelViewSet):
    serializer_class = LocationSerializer

    def get_queryset(self):
        queryset = Location.objects.filter(status__in=['pending', 'approved'])

        # Фильтрация по категории
        category = self.request.query_params.get('category')

        if category:
            queryset = queryset.filter(category_id=category)

        # Фильтрация по фильтрам
        filters = self.request.query_params.getlist('filters')

        if filters:
            filter_ids = list(map(int, filters))
            queryset = queryset.annotate(
                matched_filters=Count('locationfilter', filter=Q(locationfilter__filter_id__in=filter_ids), distinct=True)
            ).filter(matched_filters=len(filter_ids))

        return queryset.distinct()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_user(self, request):
        user_locations = Location.objects.filter(user=request.user)
        serializer = self.get_serializer(user_locations, many=True)
        return Response(serializer.data)


class LocationCategoryViewSet(ModelViewSet):
    queryset = LocationCategory.objects.all()
    serializer_class = LocationCategorySerializer

class LocationChangeViewSet(ModelViewSet):
    queryset = LocationChange.objects.all()
    serializer_class = LocationChangeSerializer

class FilterViewSet(ModelViewSet):
    queryset = Filter.objects.all()
    serializer_class = FilterSerializer
    

class LocationFilterViewSet(ModelViewSet):
    queryset = LocationFilter.objects.all()
    serializer_class = LocationFilterSerializer