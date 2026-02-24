from django.db import models
from django.conf import settings
from apps.courses.models import Course


class CBTExam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration_minutes = models.IntegerField(default=60)
    total_questions = models.IntegerField(default=0)
    pass_score = models.IntegerField(default=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = 'cbt'

    def __str__(self):
        return self.title


class Question(models.Model):
    OPTION_CHOICES = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]

    exam = models.ForeignKey(CBTExam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_option = models.CharField(max_length=1, choices=OPTION_CHOICES)
    order = models.IntegerField(default=0)

    class Meta:
        app_label = 'cbt'
        ordering = ['order']

    def __str__(self):
        return f'Q{self.order}: {self.text[:50]}'


class CBTAttempt(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('timed_out', 'Timed Out'),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cbt_attempts')
    exam = models.ForeignKey(CBTExam, on_delete=models.CASCADE, related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    time_taken_seconds = models.IntegerField(default=0)

    class Meta:
        app_label = 'cbt'

    def __str__(self):
        return f'{self.student} - {self.exam} ({self.status})'


class QuestionAnswer(models.Model):
    OPTION_CHOICES = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]

    attempt = models.ForeignKey(CBTAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    selected_option = models.CharField(max_length=1, choices=OPTION_CHOICES, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    time_taken_seconds = models.IntegerField(default=0)

    class Meta:
        app_label = 'cbt'
        unique_together = ['attempt', 'question']

    def __str__(self):
        return f'{self.attempt} - Q{self.question.order}'
