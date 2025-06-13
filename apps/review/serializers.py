from rest_framework import serializers
from .models import Photo, Review, PresenceVote


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'location', 'user', 'rating_clean', 'rating_access', 'rating_other', 'text', 'created_at']

    def validate(self, attrs):
        user = attrs.get('user')
        location = attrs.get('location')

        if Review.objects.filter(user=user, location=location).exists():
            raise serializers.ValidationError('Вы уже оставили отзыв для этой локации.')

        return super().validate(attrs)


class PhotoSerializer(serializers.ModelSerializer):
    photo_url = serializers.ReadOnlyField()

    class Meta:
        model = Photo
        fields = ['id', 'location', 'review', 'image', 'photo_url']


class PresenceVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresenceVote
        fields = ['location', 'user', 'vote']

