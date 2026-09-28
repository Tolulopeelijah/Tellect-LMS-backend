from django.contrib import admin
from .models import Course, CourseSection, Lesson, CourseEnrollment


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class CourseSectionInline(admin.TabularInline):
    model = CourseSection
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'category', 'is_published', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_published', 'category']
    search_fields = ['title', 'instructor__full_name', 'instructor__email']
    inlines = [CourseSectionInline]


@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title', 'course__title']
    autocomplete_fields = ['course']
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order']
    list_filter = ['section__course']
    search_fields = ['title', 'section__title', 'section__course__title']
    autocomplete_fields = ['section']


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at', 'progress_percentage', 'is_completed']
    list_filter = ['is_completed']
