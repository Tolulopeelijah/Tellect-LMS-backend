from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Video, VideoWatchProgress
from .serializers import VideoSerializer, VideoUploadSerializer, VideoWatchProgressSerializer


class VideosHomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "name": "Tellect LMS Videos API",
            "endpoints": {
                "course_videos": "course/<int:course_id>/",
                "upload": "upload/",
                "recently_watched": "recently-watched/",
                "video_detail": "<int:pk>/",
                "update_progress": "<int:pk>/update-progress/",
                "approve": "<int:pk>/approve/",
                "reject": "<int:pk>/reject/",
            },
        })


class CourseVideosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        videos = Video.objects.filter(course_id=course_id, status='approved')
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)


class VideoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(VideoSerializer(video).data)


class VideoUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = VideoUploadSerializer(data=request.data)
        if serializer.is_valid():
            video_file = request.data.get('video_file')
            size_mb = video_file.size / (1024 * 1024) if video_file else 0
            video = serializer.save(uploaded_by=request.user, status='pending', file_size_mb=round(size_mb, 2))
            return Response(VideoSerializer(video).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateWatchProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)

        watched_seconds = request.data.get('watched_seconds', 0)
        is_completed = video.duration_seconds > 0 and watched_seconds >= video.duration_seconds * 0.9

        progress, _ = VideoWatchProgress.objects.update_or_create(
            student=request.user,
            video=video,
            defaults={'watched_seconds': watched_seconds, 'is_completed': is_completed}
        )
        return Response(VideoWatchProgressSerializer(progress).data)


class RecentlyWatchedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        progress = VideoWatchProgress.objects.filter(student=request.user).select_related('video').order_by('-last_watched')[:10]
        serializer = VideoWatchProgressSerializer(progress, many=True)
        return Response(serializer.data)


class ApproveVideoView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)
        video.status = 'approved'
        video.rejection_reason = ''
        video.save()
        return Response({'message': 'Video approved.'})


class RejectVideoView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response({'error': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)
        reason = request.data.get('reason', '')
        video.status = 'rejected'
        video.rejection_reason = reason
        video.save()
        return Response({'message': 'Video rejected.'})
