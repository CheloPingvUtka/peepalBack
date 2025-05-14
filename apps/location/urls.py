# location/urls.py

from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, CityViewSet, LocationCategoryViewSet, LocationChangeViewSet, FilterViewSet, LocationFilterViewSet

router = DefaultRouter()

router.register(r'locations', LocationViewSet, basename='location')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'categories', LocationCategoryViewSet, basename='category')
router.register(r'location_changes', LocationChangeViewSet, basename='locationchange')
router.register(r'filters', FilterViewSet, basename='filter')
router.register(r'location_filters', LocationFilterViewSet, basename='locationfilter')

urlpatterns = router.urls


