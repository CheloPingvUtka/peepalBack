from django.contrib import admin
from .models import Location, City, LocationCategory, LocationChange, Filter, LocationFilter

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'status', 'created_at')  # Поля для отображения в списке
    search_fields = ('address', 'city__city_name')  # Поля для поиска

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'latitude', 'longitude')
    search_fields = ('city_name',)

@admin.register(LocationCategory)
class LocationCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    search_fields = ('category_name',)

@admin.register(LocationChange)
class LocationChangeAdmin(admin.ModelAdmin):
    list_display = ('location', 'field_name', 'status', 'created_at')
    search_fields = ('location__address', 'field_name')

@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = ('filter_name', 'category')
    search_fields = ('filter_name',)

@admin.register(LocationFilter)
class LocationFilterAdmin(admin.ModelAdmin):
    list_display = ('location', 'filter')
