from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Photo, PresenceVote
from rest_framework import status
from rest_framework.response import Response
from .serializers import PhotoSerializer, ReviewSerializer, PresenceVoteSerializer
from .models import Review
from rest_framework.decorators import api_view
from django.db.models import Prefetch
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q, F
from apps.location.models import Location


@api_view(['GET'])
def public_reviews_by_user(request, user_id):
    reviews = Review.objects.filter(user_id=user_id).exclude(location__user_id=user_id).select_related('location')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


class UserReviewListView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).exclude(location__user=self.request.user).select_related('location')


@api_view(['GET'])
def get_reviews_by_location(request, location_id):
    reviews = Review.objects.filter(location_id=location_id).select_related('user')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


class ReviewCreateAPIView(APIView):
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PresenceVoteAPIView(APIView):
    def post(self, request):
        location = request.data.get('location')
        user = request.data.get('user')
        vote = request.data.get('vote')

        if vote not in ['present', 'absent']:
            return Response({'error': 'Недопустимое значение vote'}, status=400)

        existing_vote = PresenceVote.objects.filter(location_id=location, user_id=user).first()

        if existing_vote:
            if existing_vote.vote != vote:
                existing_vote.vote = vote
                existing_vote.save()
        else:
            PresenceVote.objects.create(location_id=location, user_id=user, vote=vote)

        # После голосования — проверяем стоит ли отклонить локацию
        present_count = PresenceVote.objects.filter(location_id=location, vote='present').count()
        absent_count = PresenceVote.objects.filter(location_id=location, vote='absent').count()

        if absent_count >= 5 or (absent_count > 0 and present_count < absent_count * 2):
            Location.objects.filter(id=location).update(status='rejected')

        return Response({'message': 'Голос засчитан'}, status=200)
    

class PresenceStatsAPIView(APIView):
    def get(self, request, location_id):
        present_count = PresenceVote.objects.filter(location_id=location_id, vote='present').count()
        absent_count = PresenceVote.objects.filter(location_id=location_id, vote='absent').count()

        return Response({
            'present': present_count,
            'absent': absent_count
        })

    
class PhotoListView(ListAPIView):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        queryset = Photo.objects.all()
        location_id = self.request.query_params.get('location')
        if location_id:
            queryset = queryset.filter(location_id=location_id)
        return queryset


class MultiPhotoUploadAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        location_id = request.data.get('location')
        review_id = request.data.get('review')

        files = request.FILES.getlist('images')  # <-- ожидаем ключ 'images'
        if not files:
            return Response({'error': 'No files provided.'}, status=400)

        photos = []
        for file in files:
            photo = Photo(
                image=file,
                location_id=location_id,
                review_id=review_id if review_id else None
            )
            photo.save()
            photos.append(photo)

        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status=201)



class PhotoUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)