from django.contrib import admin
from .models import PDFMaterial, PDFReadProgress


@admin.register(PDFMaterial)
class PDFMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'is_downloadable', 'uploaded_by', 'created_at']
    list_filter = ['is_downloadable', 'created_at']
    search_fields = ['title']
    autocomplete_fields = ['lesson']


@admin.register(PDFReadProgress)
class PDFReadProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'pdf', 'pages_read', 'total_pages', 'is_completed']
