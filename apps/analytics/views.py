from django.utils import timezone
from django.db.models import Avg, Sum, Q
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.authentication.permissions import IsAdmin, IsInstructorOrAdmin
from apps.authentication.models import User
from apps.courses.models import Course, CourseEnrollment
from apps.videos.models import VideoWatchProgress
from apps.pdfs.models import PDFReadProgress
from apps.cbt.models import CBTAttempt
from apps.payments.models import Transaction


class AnalyticsHomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'name': 'Tellect LMS Analytics API',
            'status': 'active',
            'endpoints': {
                'overview': 'overview/',
                'course': 'course/<course_id>/',
                'platform': 'platform/',
            },
        })


class StudentOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        enrollments = CourseEnrollment.objects.filter(student=user)
        video_progress = VideoWatchProgress.objects.filter(student=user)
        pdf_progress = PDFReadProgress.objects.filter(student=user)
        cbt_attempts = CBTAttempt.objects.filter(student=user, status='submitted')

        return Response({
            'enrollments': {
                'total': enrollments.count(),
                'completed': enrollments.filter(is_completed=True).count(),
                'average_progress': round(enrollments.aggregate(avg=Avg('progress_percentage'))['avg'] or 0, 1),
            },
            'videos': {
                'total_watched': video_progress.filter(is_completed=True).count(),
                'total_watch_seconds': video_progress.aggregate(total=Sum('watched_seconds'))['total'] or 0,
            },
            'pdfs': {
                'total_read': pdf_progress.filter(is_completed=True).count(),
                'total_time_minutes': pdf_progress.aggregate(total=Sum('time_spent_minutes'))['total'] or 0,
            },
            'cbt': {
                'total_attempts': cbt_attempts.count(),
                'average_score': round(cbt_attempts.aggregate(avg=Avg('score'))['avg'] or 0, 1),
                'pass_rate': self._pass_rate(cbt_attempts),
            },
        })

    def _pass_rate(self, attempts):
        if not attempts.exists():
            return 0
        passed = sum(1 for a in attempts if a.score >= a.exam.pass_score)
        return round(passed / attempts.count() * 100, 1)


class CourseAnalyticsView(APIView):
    permission_classes = [IsInstructorOrAdmin]

    def get(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id, is_active=True)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role == 'INSTRUCTOR' and course.instructor != request.user:
            return Response({'error': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)

        enrollments = CourseEnrollment.objects.filter(course=course)
        return Response({
            'course': {'id': course.id, 'title': course.title},
            'enrollments': {
                'total': enrollments.count(),
                'completed': enrollments.filter(is_completed=True).count(),
                'average_progress': round(enrollments.aggregate(avg=Avg('progress_percentage'))['avg'] or 0, 1),
            },
            'recent_enrollments': [
                {
                    'student': e.student.full_name,
                    'enrolled_at': e.enrolled_at.isoformat(),
                    'progress_percentage': e.progress_percentage,
                }
                for e in enrollments.order_by('-enrolled_at')[:10]
            ],
        })


class PlatformAnalyticsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({
            'users': {
                'total': User.objects.filter(is_active=True).count(),
                'students': User.objects.filter(role='STUDENT', is_active=True).count(),
                'instructors': User.objects.filter(role='INSTRUCTOR', is_active=True).count(),
                'admins': User.objects.filter(role='ADMIN', is_active=True).count(),
            },
            'courses': {
                'total': Course.objects.filter(is_active=True).count(),
                'published': Course.objects.filter(is_active=True, is_published=True).count(),
            },
            'enrollments': CourseEnrollment.objects.count(),
            'revenue': {
                'total_transactions': Transaction.objects.filter(status='SUCCESS').count(),
                'total_amount': str(
                    Transaction.objects.filter(status='SUCCESS').aggregate(total=Sum('amount'))['total'] or 0
                ),
            },
            'generated_at': timezone.now().isoformat(),
        })
