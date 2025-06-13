from django.urls import path
from .views import PhotoUploadView, PhotoListView, MultiPhotoUploadAPIView, ReviewCreateAPIView, PresenceVoteAPIView, PresenceStatsAPIView


urlpatterns = [
    path('', PhotoListView.as_view(), name='photo-list'),
    path('presence/vote/', PresenceVoteAPIView.as_view(), name='presence-vote'),
    path('presence/stats/<int:location_id>/', PresenceStatsAPIView.as_view(), name='presence-stats'),
    path('photos/', PhotoListView.as_view()),
    path('upload-photo/', PhotoUploadView.as_view(), name='upload-photo'),
    path('upload-multiple/', MultiPhotoUploadAPIView.as_view(), name='upload-multiple'),
    path('create/', ReviewCreateAPIView.as_view(), name='review-create'),
]

