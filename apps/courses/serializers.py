from rest_framework import serializers
from .models import Course, CourseEnrollment


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'thumbnail', 'instructor', 'created_at', 'is_active']


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = CourseEnrollment
        fields = ['id', 'course', 'enrolled_at', 'progress_percentage', 'is_completed']
