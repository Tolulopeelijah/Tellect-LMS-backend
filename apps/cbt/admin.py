from django.contrib import admin
from .models import CBTExam, Question, CBTAttempt, QuestionAnswer


@admin.register(CBTExam)
class CBTExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'duration_minutes', 'total_questions', 'pass_score', 'is_active']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['exam', 'text', 'correct_option', 'order']


@admin.register(CBTAttempt)
class CBTAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'status', 'score', 'started_at']


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'selected_option', 'is_correct']
