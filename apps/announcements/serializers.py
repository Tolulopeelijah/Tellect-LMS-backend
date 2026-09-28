from rest_framework import serializers
from apps.authentication.serializers import UserProfileSerializer
from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    author_details = UserProfileSerializer(source='author', read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'content', 'author', 'author_details',
            'target_audience', 'is_published', 'created_at', 'expires_at',
            'is_active',
        ]
        read_only_fields = ['id', 'author', 'created_at']
