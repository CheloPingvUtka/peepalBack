from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.authentication.urls')),
    path('api/locations/', include('apps.location.urls')),
    path('api/reviews/', include('apps.review.urls')),
    path('api/user/', include('apps.user.urls')),
]
