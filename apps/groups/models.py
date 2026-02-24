from django.db import models
from django.conf import settings


class StudyGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='GroupMembership', related_name='study_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = 'groups'

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    ROLE_CHOICES = [('member', 'Member'), ('admin', 'Admin')]

    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='memberships')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_memberships')
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')

    class Meta:
        app_label = 'groups'
        unique_together = ['group', 'student']

    def __str__(self):
        return f'{self.student} in {self.group} ({self.role})'
