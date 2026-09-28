from django.contrib import admin
from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_number', 'student', 'course', 'issued_at', 'is_valid')
    search_fields = ('certificate_number', 'verification_code', 'student__email')
    list_filter = ('is_valid',)
