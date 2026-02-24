from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.courses.models import CourseEnrollment
from apps.courses.serializers import CourseEnrollmentSerializer
from apps.videos.models import VideoWatchProgress
from apps.videos.serializers import VideoWatchProgressSerializer
from apps.pdfs.models import PDFReadProgress
from .models import ReadingTimetable, TodoItem
from .serializers import ReadingTimetableSerializer, TodoItemSerializer


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().weekday()

        enrollments = CourseEnrollment.objects.filter(student=user).select_related('course')
        recent_videos = VideoWatchProgress.objects.filter(student=user).select_related('video').order_by('-last_watched')[:5]
        pdf_progress = PDFReadProgress.objects.filter(student=user)
        total_pdfs_read = pdf_progress.filter(is_completed=True).count()
        total_time_reading = sum(p.time_spent_minutes for p in pdf_progress)
        todays_timetable = ReadingTimetable.objects.filter(student=user, day_of_week=today, is_active=True)
        todos = TodoItem.objects.filter(student=user, scheduled_date=timezone.now().date())

        return Response({
            'enrolled_courses': CourseEnrollmentSerializer(enrollments, many=True).data,
            'recently_watched': VideoWatchProgressSerializer(recent_videos, many=True).data,
            'pdf_stats': {'total_pdfs_read': total_pdfs_read, 'total_time_spent_minutes': total_time_reading},
            'todays_timetable': ReadingTimetableSerializer(todays_timetable, many=True).data,
            'todays_todos': TodoItemSerializer(todos, many=True).data,
        })


class TimetableView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        entries = ReadingTimetable.objects.filter(student=request.user)
        return Response(ReadingTimetableSerializer(entries, many=True).data)

    def post(self, request):
        serializer = ReadingTimetableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimetableDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_object(self, pk, user):
        try:
            return ReadingTimetable.objects.get(pk=pk, student=user)
        except ReadingTimetable.DoesNotExist:
            return None

    def put(self, request, pk):
        entry = self._get_object(pk, request.user)
        if not entry:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReadingTimetableSerializer(entry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        entry = self._get_object(pk, request.user)
        if not entry:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TodoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        todos = TodoItem.objects.filter(student=request.user)
        return Response(TodoItemSerializer(todos, many=True).data)

    def post(self, request):
        serializer = TodoItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_object(self, pk, user):
        try:
            return TodoItem.objects.get(pk=pk, student=user)
        except TodoItem.DoesNotExist:
            return None

    def put(self, request, pk):
        todo = self._get_object(pk, request.user)
        if not todo:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TodoItemSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        todo = self._get_object(pk, request.user)
        if not todo:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CompleteTodoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            todo = TodoItem.objects.get(pk=pk, student=request.user)
        except TodoItem.DoesNotExist:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        todo.is_completed = True
        todo.save()
        return Response({'message': 'Todo marked as complete.'})
