from rest_framework import serializers
from .models import VideoSection, Video, VideoWatchProgress


class VideoSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoSection
        fields = ['id', 'title', 'order']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'section', 'course', 'title', 'description', 'video_file', 'thumbnail',
                  'duration_seconds', 'is_downloadable', 'status', 'rejection_reason',
                  'uploaded_by', 'created_at', 'file_size_mb']
        read_only_fields = ['status', 'rejection_reason', 'uploaded_by', 'created_at']


class VideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['course', 'section', 'title', 'description', 'video_file', 'thumbnail', 'is_downloadable']

    def validate_video_file(self, value):
        allowed_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv']
        name = value.name.lower()
        if not any(name.endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError('Invalid video file type.')
        size_mb = value.size / (1024 * 1024)
        if size_mb > 2048:
            raise serializers.ValidationError('File size exceeds 2GB limit.')
        return value


class VideoWatchProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoWatchProgress
        fields = ['id', 'video', 'watched_seconds', 'last_watched', 'is_completed']
        read_only_fields = ['video', 'last_watched']
