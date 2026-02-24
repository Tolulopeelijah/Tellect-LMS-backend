from django.db import models
from django.conf import settings
from apps.courses.models import Course


class PDFMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='pdfs')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='pdfs/')
    is_downloadable = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_pdfs')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'pdfs'

    def __str__(self):
        return self.title


class PDFReadProgress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pdf_progress')
    pdf = models.ForeignKey(PDFMaterial, on_delete=models.CASCADE, related_name='read_progress')
    pages_read = models.IntegerField(default=0)
    total_pages = models.IntegerField(default=0)
    time_spent_minutes = models.IntegerField(default=0)
    last_read = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        app_label = 'pdfs'
        unique_together = ['student', 'pdf']

    def __str__(self):
        return f'{self.student} reading {self.pdf}'
