from django.urls import path
from .views import CourseListView, CourseDetailView, EnrollCourseView, MyCoursesView

urlpatterns = [
    path('', CourseListView.as_view(), name='course-list'),
    path('my-courses/', MyCoursesView.as_view(), name='my-courses'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('<int:pk>/enroll/', EnrollCourseView.as_view(), name='course-enroll'),
]
