from django.urls import path
from .views import (
    AnalyticsHomeView,
    StudentOverviewView,
    CourseAnalyticsView,
    PlatformAnalyticsView,
)

urlpatterns = [
    path('', AnalyticsHomeView.as_view(), name='analytics-home'),
    path('overview/', StudentOverviewView.as_view(), name='analytics-overview'),
    path('course/<int:course_id>/', CourseAnalyticsView.as_view(), name='analytics-course'),
    path('platform/', PlatformAnalyticsView.as_view(), name='analytics-platform'),
]
