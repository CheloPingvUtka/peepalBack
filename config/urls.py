# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('auth/')),
    path('auth/', include('apps.authentication.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('apps.location.urls')),
]


