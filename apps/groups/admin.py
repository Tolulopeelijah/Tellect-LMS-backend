from django.contrib import admin
from .models import StudyGroup, GroupMembership


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'is_active', 'created_at']


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ['group', 'student', 'role', 'joined_at']
