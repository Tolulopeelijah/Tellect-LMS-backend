from django.db import models
from django.conf import settings
from apps.courses.models import Course


class VideoSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    class Meta:
        app_label = 'videos'
        ordering = ['order']

    def __str__(self):
        return f'{self.course.title} - {self.title}'


class Video(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    section = models.ForeignKey(VideoSection, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    duration_seconds = models.IntegerField(default=0)
    is_downloadable = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_videos')
    created_at = models.DateTimeField(auto_now_add=True)
    file_size_mb = models.FloatField(default=0)

    class Meta:
        app_label = 'videos'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class VideoWatchProgress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watch_progress')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='watch_progress')
    watched_seconds = models.IntegerField(default=0)
    last_watched = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        app_label = 'videos'
        unique_together = ['student', 'video']

    def __str__(self):
        return f'{self.student} watching {self.video}'
