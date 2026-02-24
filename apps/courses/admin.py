from django.contrib import admin
from .models import Course, CourseEnrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['title', 'instructor']


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at', 'progress_percentage', 'is_completed']
    list_filter = ['is_completed']
