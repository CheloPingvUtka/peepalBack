from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Photo
from rest_framework import status
from rest_framework.response import Response
from .serializers import PhotoSerializer


class PhotoUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class PhotoListView(ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


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
