from rest_framework import serializers
from apps.authentication.serializers import UserProfileSerializer
from .models import SupportTicket, TicketReply


class TicketReplySerializer(serializers.ModelSerializer):
    sender_details = UserProfileSerializer(source='sender', read_only=True)

    class Meta:
        model = TicketReply
        fields = [
            'id', 'sender', 'sender_details', 'message',
            'is_staff_reply', 'created_at',
        ]
        read_only_fields = ['id', 'sender', 'is_staff_reply', 'created_at']


class SupportTicketSerializer(serializers.ModelSerializer):
    user_details = UserProfileSerializer(source='user', read_only=True)
    replies = TicketReplySerializer(many=True, read_only=True)

    class Meta:
        model = SupportTicket
        fields = [
            'id', 'user', 'user_details', 'subject', 'description',
            'status', 'priority', 'created_at', 'updated_at', 'replies',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class SupportTicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ['subject', 'description', 'priority']


class TicketReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketReply
        fields = ['message']
