from rest_framework import serializers
from apps.authentication.serializers import UserProfileSerializer
from .models import StudyGroup, GroupMembership


class GroupMembershipSerializer(serializers.ModelSerializer):
    student = UserProfileSerializer(read_only=True)

    class Meta:
        model = GroupMembership
        fields = ['id', 'student', 'joined_at', 'role']


class StudyGroupSerializer(serializers.ModelSerializer):
    memberships = GroupMembershipSerializer(many=True, read_only=True)
    created_by = UserProfileSerializer(read_only=True)

    class Meta:
        model = StudyGroup
        fields = ['id', 'name', 'description', 'created_by', 'memberships', 'created_at', 'is_active']
        read_only_fields = ['created_by', 'created_at']


class StudyGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyGroup
        fields = ['name', 'description']
