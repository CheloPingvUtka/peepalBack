from django.contrib import admin
from .models import Review, Photo, PresenceVote

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass

@admin.register(PresenceVote)
class PresenceVoteAdmin(admin.ModelAdmin):
    pass