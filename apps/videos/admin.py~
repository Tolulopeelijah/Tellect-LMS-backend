from django.contrib import admin
from .models import VideoSection, Video, VideoWatchProgress


@admin.register(VideoSection)
class VideoSectionAdmin(admin.ModelAdmin):
    list_display = ['course', 'title', 'order']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'status', 'uploaded_by', 'created_at']
    list_filter = ['status']
    search_fields = ['title']


@admin.register(VideoWatchProgress)
class VideoWatchProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'video', 'watched_seconds', 'is_completed']
