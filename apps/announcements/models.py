from django.db import models
from django.conf import settings
from django.utils import timezone


class Announcement(models.Model):
    AUDIENCE_CHOICES = [
        ('ALL', 'All Users'),
        ('STUDENTS', 'Students'),
        ('INSTRUCTORS', 'Instructors'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='announcements',
    )
    target_audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default='ALL')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'announcements'
        ordering = ['-created_at']

    def is_active(self):
        if not self.is_published:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True

    def __str__(self):
        return self.title
