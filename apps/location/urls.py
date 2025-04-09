# apps/location/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'locationcategories', LocationCategoryViewSet, basename='locationcategory')
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'locationchanges', LocationChangeViewSet, basename='locationchange')
router.register(r'filters', FilterViewSet, basename='filter')
router.register(r'locationfilters', LocationFilterViewSet, basename='locationfilter')

urlpatterns = [
    path('', include(router.urls)),
]
