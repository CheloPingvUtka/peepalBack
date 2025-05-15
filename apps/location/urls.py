# location/urls.py

from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, LocationCategoryViewSet

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'categories', LocationCategoryViewSet, basename='category')

urlpatterns = router.urls
