import uuid
from django.db import models
from django.conf import settings
from apps.courses.models import Course


class Certificate(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='certificates',
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    certificate_number = models.CharField(max_length=50, unique=True)
    verification_code = models.CharField(max_length=32, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    is_valid = models.BooleanField(default=True)

    class Meta:
        app_label = 'certificates'
        unique_together = ['student', 'course']
        ordering = ['-issued_at']

    def save(self, *args, **kwargs):
        if not self.certificate_number:
            self.certificate_number = f'TLC-{uuid.uuid4().hex[:10].upper()}'
        if not self.verification_code:
            self.verification_code = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.student.email} - {self.course.title}'
