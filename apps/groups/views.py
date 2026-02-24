from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.pdfs.models import PDFReadProgress
from apps.cbt.models import CBTAttempt
from .models import StudyGroup, GroupMembership
from .serializers import StudyGroupSerializer, StudyGroupCreateSerializer, GroupMembershipSerializer


class GroupListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        groups = StudyGroup.objects.filter(is_active=True)
        return Response(StudyGroupSerializer(groups, many=True).data)

    def post(self, request):
        serializer = StudyGroupCreateSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save(created_by=request.user)
            GroupMembership.objects.create(group=group, student=request.user, role='admin')
            return Response(StudyGroupSerializer(group).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            group = StudyGroup.objects.get(pk=pk, is_active=True)
        except StudyGroup.DoesNotExist:
            return Response({'error': 'Group not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(StudyGroupSerializer(group).data)


class JoinGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            group = StudyGroup.objects.get(pk=pk, is_active=True)
        except StudyGroup.DoesNotExist:
            return Response({'error': 'Group not found.'}, status=status.HTTP_404_NOT_FOUND)

        membership, created = GroupMembership.objects.get_or_create(group=group, student=request.user)
        if not created:
            return Response({'message': 'Already a member.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Joined group successfully.'}, status=status.HTTP_201_CREATED)


class LeaveGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            membership = GroupMembership.objects.get(group_id=pk, student=request.user)
        except GroupMembership.DoesNotExist:
            return Response({'error': 'You are not a member of this group.'}, status=status.HTTP_400_BAD_REQUEST)
        membership.delete()
        return Response({'message': 'Left group successfully.'})


class MembersProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            group = StudyGroup.objects.get(pk=pk, is_active=True)
        except StudyGroup.DoesNotExist:
            return Response({'error': 'Group not found.'}, status=status.HTTP_404_NOT_FOUND)

        members_data = []
        for membership in group.memberships.select_related('student'):
            student = membership.student
            pdf_progress = PDFReadProgress.objects.filter(student=student)
            recent_attempts = CBTAttempt.objects.filter(student=student, status='submitted').order_by('-submitted_at')[:5]
            members_data.append({
                'student': {'id': student.id, 'full_name': student.full_name, 'email': student.email},
                'role': membership.role,
                'pdf_stats': {
                    'total_pdfs_read': pdf_progress.filter(is_completed=True).count(),
                    'total_time_spent_minutes': sum(p.time_spent_minutes for p in pdf_progress),
                },
                'recent_cbt_scores': [{'exam': a.exam.title, 'score': a.score} for a in recent_attempts],
            })
        return Response(members_data)
