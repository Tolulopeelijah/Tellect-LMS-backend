from rest_framework import serializers
from apps.authentication.serializers import UserProfileSerializer
from .models import Category, Course, CourseSection, Lesson, CourseEnrollment, LessonProgress

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSectionSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = CourseSection
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    instructor_details = UserProfileSerializer(source='instructor', read_only=True)
    category_details = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'thumbnail', 'instructor', 'instructor_details',
            'category', 'category_details', 'price', 'is_published', 'created_at', 'is_active'
        ]
        read_only_fields = ['instructor']

class CourseDetailSerializer(CourseSerializer):
    sections = CourseSectionSerializer(many=True, read_only=True)

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['sections']

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = CourseEnrollment
        fields = ['id', 'student', 'course', 'enrolled_at', 'progress_percentage', 'is_completed']
        read_only_fields = ['student', 'progress_percentage', 'is_completed']

class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = '__all__'
