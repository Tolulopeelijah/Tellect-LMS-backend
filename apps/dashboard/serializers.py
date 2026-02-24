from rest_framework import serializers
from .models import ReadingTimetable, TodoItem


class ReadingTimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingTimetable
        fields = ['id', 'day_of_week', 'start_time', 'end_time', 'subject', 'is_active']


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ['id', 'title', 'description', 'scheduled_time', 'scheduled_date', 'is_completed', 'created_at']
        read_only_fields = ['created_at']
