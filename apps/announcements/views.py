from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.authentication.permissions import IsInstructorOrAdmin
from .models import Announcement
from .serializers import AnnouncementSerializer


class AnnouncementsHomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'name': 'Tellect LMS Announcements API',
            'status': 'active',
            'endpoints': {
                'list': 'list/',
                'create': 'create/',
                'detail': '<id>/',
            },
        })


class AnnouncementListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        now = timezone.now()
        announcements = Announcement.objects.filter(is_published=True)
        announcements = announcements.filter(
            models_q_expired(now)
        )
        if request.user.is_authenticated:
            role = request.user.role
            if role == 'STUDENT':
                announcements = announcements.filter(target_audience__in=['ALL', 'STUDENTS'])
            elif role == 'INSTRUCTOR':
                announcements = announcements.filter(target_audience__in=['ALL', 'INSTRUCTORS'])
        else:
            announcements = announcements.filter(target_audience='ALL')
        return Response(AnnouncementSerializer(announcements, many=True).data)


def models_q_expired(now):
    from django.db.models import Q
    return Q(expires_at__isnull=True) | Q(expires_at__gt=now)


class AnnouncementCreateView(APIView):
    permission_classes = [IsInstructorOrAdmin]

    def post(self, request):
        serializer = AnnouncementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnnouncementDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsInstructorOrAdmin()]

    def _get_object(self, pk):
        try:
            return Announcement.objects.get(pk=pk)
        except Announcement.DoesNotExist:
            return None

    def get(self, request, pk):
        announcement = self._get_object(pk)
        if not announcement:
            return Response({'error': 'Announcement not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(AnnouncementSerializer(announcement).data)

    def put(self, request, pk):
        announcement = self._get_object(pk)
        if not announcement:
            return Response({'error': 'Announcement not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AnnouncementSerializer(announcement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        announcement = self._get_object(pk)
        if not announcement:
            return Response({'error': 'Announcement not found.'}, status=status.HTTP_404_NOT_FOUND)
        announcement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
