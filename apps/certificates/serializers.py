from rest_framework import serializers
from apps.authentication.serializers import UserProfileSerializer
from apps.courses.serializers import CourseSerializer
from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    student_details = UserProfileSerializer(source='student', read_only=True)
    course_details = CourseSerializer(source='course', read_only=True)

    class Meta:
        model = Certificate
        fields = [
            'id', 'student', 'student_details', 'course', 'course_details',
            'certificate_number', 'verification_code', 'issued_at',
            'pdf_file', 'is_valid',
        ]
        read_only_fields = [
            'id', 'student', 'certificate_number', 'verification_code',
            'issued_at', 'is_valid',
        ]


class CertificateVerifySerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Certificate
        fields = [
            'certificate_number', 'verification_code', 'student_name',
            'course_title', 'issued_at', 'is_valid',
        ]
