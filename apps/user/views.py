from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.review.models import Review
from apps.location.models import Location


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats(request):
    user = request.user

    reviews_count = Review.objects.filter(user=user).count()
    pending_locations_count = Location.objects.filter(user=user, status='pending').count()

    return Response({
        'reviews_count': reviews_count,
        'pending_locations_count': pending_locations_count,
    })
