from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, CourseViewSet, CourseSectionViewSet, LessonViewSet, MyCoursesViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'sections', CourseSectionViewSet, basename='coursesection')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'my-courses', MyCoursesViewSet, basename='mycourses')
router.register(r'', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
]
