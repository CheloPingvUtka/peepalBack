from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from django.db.models import Count
from .models import LocationCategory, Location, LocationChange, Filter, LocationFilter
from .serializers import LocationCategorySerializer, LocationLightSerializer, LocationSerializer, LocationChangeSerializer, FilterSerializer, LocationFilterSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from django.db.models.functions import ACos, Cos, Sin, Radians
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


@method_decorator(cache_page(60 * 5), name='dispatch')  # кэш 5 минут
class LocationViewSet(ModelViewSet):
    serializer_class = LocationSerializer

    def get_queryset(self):

        queryset = Location.objects.filter(status__in=['pending', 'approved'])

        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')
        radius = self.request.query_params.get('radius', 5)

        if lat and lon:
            try:
                lat = float(lat)
                lon = float(lon)
                radius = float(radius)

                # Пример грубой фильтрации через прямое расстояние по градусам
                delta = radius / 111  # ~1° = 111 км
                queryset = queryset.filter(
                    latitude__range=(lat - delta, lat + delta),
                    longitude__range=(lon - delta, lon + delta)
                )
            except ValueError:
                pass

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


    @action(detail=False, methods=['get'], url_path='light')
    def light_locations(self, request):
        queryset = self.get_queryset()
        serializer = LocationLightSerializer(queryset, many=True)
        return Response(serializer.data)
    

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_user(self, request):
        user_locations = Location.objects.filter(user=request.user)
        serializer = self.get_serializer(user_locations, many=True)
        return Response(serializer.data)
    

    @action(detail=False, methods=['get'], url_path='public/by-user/(?P<user_id>[^/.]+)')
    def public_by_user(self, request, user_id=None):
        locations = Location.objects.filter(user_id=user_id)
        serializer = self.get_serializer(locations, many=True)
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