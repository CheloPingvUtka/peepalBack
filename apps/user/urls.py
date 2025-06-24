from django.urls import path
from .views import user_stats

urlpatterns = [
    path('stats/', user_stats, name='user-stats'),
]
