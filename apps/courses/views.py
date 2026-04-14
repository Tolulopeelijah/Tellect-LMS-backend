from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from apps.authentication.permissions import IsInstructorOrAdmin
from .models import Category, Course, CourseSection, Lesson, CourseEnrollment, LessonProgress
from .serializers import (
    CategorySerializer, CourseSerializer, CourseDetailSerializer, 
    CourseSectionSerializer, LessonSerializer, CourseEnrollmentSerializer,
    LessonProgressSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsInstructorOrAdmin]
        return [permission() for permission in permission_classes]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_published']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsInstructorOrAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True)
        if self.action == 'list' and not (self.request.user.is_authenticated and self.request.user.role in ['ADMIN', 'INSTRUCTOR']):
            queryset = queryset.filter(is_published=True)
        return queryset

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def enroll(self, request, pk=None):
        course = self.get_object()
        
        # Payment integration required for non-free courses. 
        # For MVP we allow direct enrollment logic assuming it's free or handled separately.
        if course.price > 0:
            return Response({'error': 'Payment required to enroll in this course.'}, status=status.HTTP_402_PAYMENT_REQUIRED)

        enrollment, created = CourseEnrollment.objects.get_or_create(student=request.user, course=course)
        if not created:
            return Response({'message': 'Already enrolled.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Enrolled successfully.', 'enrollment': CourseEnrollmentSerializer(enrollment).data}, status=status.HTTP_201_CREATED)


class CourseSectionViewSet(viewsets.ModelViewSet):
    queryset = CourseSection.objects.all()
    serializer_class = CourseSectionSerializer
    permission_classes = [IsInstructorOrAdmin]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsInstructorOrAdmin]


class MyCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CourseEnrollment.objects.filter(student=self.request.user).select_related('course')
