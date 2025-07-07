from rest_framework import serializers
from .models import Location, LocationCategory, LocationChange, Filter, LocationFilter
from apps.user.models import User  # проверь, что путь правильный




class LocationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCategory
        fields = ['id', 'category_name']

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class LocationSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField()
    rating = serializers.SerializerMethodField()
    # READ-ONLY часть
    filters = serializers.SerializerMethodField()

    # WRITE-ONLY поля
    filters_ids = serializers.PrimaryKeyRelatedField(
        queryset=Filter.objects.all(), many=True, write_only=True, source='filters'
    )

    category = LocationCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=LocationCategory.objects.all(), write_only=True)

    user = UserShortSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Location
        fields = [
            'id', 'address', 'description', 'status',
            'latitude', 'longitude', 'created_at', 'updated_at',
            'city_name',
            'category', 'category_id',
            'user', 'user_id',
            'filters', 'filters_ids',
            'rating',
        ]

    def get_rating(self, obj):
            from apps.review.models import Review
            reviews = Review.objects.filter(location=obj)
            if not reviews.exists():
                return None
            count = reviews.count()
            return {
                'total': round((
                    sum(r.rating_clean + r.rating_access + (r.rating_other or 0) for r in reviews)
                ) / (count * 3), 1),
                'clean': round(sum(r.rating_clean for r in reviews) / count, 1),
                'comfort': round(sum(r.rating_access for r in reviews) / count, 1),
                'other': round(sum((r.rating_other or 0) for r in reviews) / count, 1),
            }

    def get_filters(self, obj):
        return FilterShortSerializer(
            Filter.objects.filter(locationfilter__location=obj), many=True
        ).data

    def create(self, validated_data):
        # Извлекаем filters, category_id и user_id
        filters = validated_data.pop('filters', [])
        category = validated_data.pop('category_id')
        user = validated_data.pop('user_id')

        location = Location.objects.create(
            category=category,
            user=user,
            **validated_data
        )

        for f in filters:
            LocationFilter.objects.create(location=location, filter=f)

        return location

class LocationChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationChange
        fields = '__all__' 

class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = '__all__' 

class LocationFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationFilter
        fields = '__all__'  

class FilterShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = ['id', 'filter_name']


class LocationLightSerializer(serializers.ModelSerializer):
    category = LocationCategorySerializer(read_only=True)
    filters = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ['id', 'latitude', 'longitude', 'category', 'filters']

    def get_filters(self, obj):
        return FilterShortSerializer(
            Filter.objects.filter(locationfilter__location=obj), many=True
        ).data