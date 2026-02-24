from rest_framework import serializers
from .models import PDFMaterial, PDFReadProgress


class PDFMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFMaterial
        fields = ['id', 'course', 'title', 'description', 'pdf_file', 'is_downloadable', 'uploaded_by', 'created_at']
        read_only_fields = ['uploaded_by', 'created_at']


class PDFReadProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFReadProgress
        fields = ['id', 'pdf', 'pages_read', 'total_pages', 'time_spent_minutes', 'last_read', 'is_completed']
        read_only_fields = ['pdf', 'last_read']
