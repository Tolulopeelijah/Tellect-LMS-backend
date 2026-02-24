from django.contrib import admin
from .models import ReadingTimetable, TodoItem


@admin.register(ReadingTimetable)
class ReadingTimetableAdmin(admin.ModelAdmin):
    list_display = ['student', 'day_of_week', 'start_time', 'end_time', 'subject', 'is_active']


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ['student', 'title', 'scheduled_date', 'is_completed']
