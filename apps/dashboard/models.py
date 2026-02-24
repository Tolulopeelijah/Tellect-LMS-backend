from django.db import models
from django.conf import settings


class ReadingTimetable(models.Model):
    DAY_CHOICES = [(i, day) for i, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='timetable_entries')
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = 'dashboard'

    def __str__(self):
        return f'{self.student} - {self.get_day_of_week_display()} {self.subject}'


class TodoItem(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='todos')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    scheduled_time = models.TimeField(null=True, blank=True)
    scheduled_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'dashboard'
        ordering = ['scheduled_date', 'scheduled_time']

    def __str__(self):
        return self.title
