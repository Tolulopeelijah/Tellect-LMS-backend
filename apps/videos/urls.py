from django.urls import path
from .views import CourseVideosView, VideoDetailView, VideoUploadView, UpdateWatchProgressView, RecentlyWatchedView, ApproveVideoView, RejectVideoView

urlpatterns = [
    path('course/<int:course_id>/', CourseVideosView.as_view(), name='course-videos'),
    path('upload/', VideoUploadView.as_view(), name='video-upload'),
    path('recently-watched/', RecentlyWatchedView.as_view(), name='recently-watched'),
    path('<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('<int:pk>/update-progress/', UpdateWatchProgressView.as_view(), name='video-update-progress'),
    path('<int:pk>/approve/', ApproveVideoView.as_view(), name='video-approve'),
    path('<int:pk>/reject/', RejectVideoView.as_view(), name='video-reject'),
]
