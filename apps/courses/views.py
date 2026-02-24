from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Course, CourseEnrollment
from .serializers import CourseSerializer, CourseEnrollmentSerializer


class CourseListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        courses = Course.objects.filter(is_active=True)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class CourseDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk, is_active=True)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

        data = CourseSerializer(course).data
        if request.user.is_authenticated:
            enrollment = CourseEnrollment.objects.filter(student=request.user, course=course).first()
            if enrollment:
                data['enrollment'] = CourseEnrollmentSerializer(enrollment).data
        return Response(data)


class EnrollCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            course = Course.objects.get(pk=pk, is_active=True)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

        enrollment, created = CourseEnrollment.objects.get_or_create(student=request.user, course=course)
        if not created:
            return Response({'message': 'Already enrolled.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Enrolled successfully.', 'enrollment': CourseEnrollmentSerializer(enrollment).data}, status=status.HTTP_201_CREATED)


class MyCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enrollments = CourseEnrollment.objects.filter(student=request.user).select_related('course')
        serializer = CourseEnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
