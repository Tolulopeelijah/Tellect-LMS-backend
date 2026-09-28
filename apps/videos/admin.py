from django.contrib import admin
from .models import Video, VideoWatchProgress

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'status', 'uploaded_by', 'created_at']
    list_filter = ['status']
    search_fields = ['title']
    autocomplete_fields = ['lesson']


@admin.register(VideoWatchProgress)
class VideoWatchProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'video', 'watched_seconds', 'is_completed']
