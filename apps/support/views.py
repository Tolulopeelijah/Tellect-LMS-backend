from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.authentication.permissions import IsAdmin
from .models import SupportTicket, TicketReply
from .serializers import (
    SupportTicketSerializer,
    SupportTicketCreateSerializer,
    TicketReplyCreateSerializer,
    TicketReplySerializer,
)


class SupportHomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'name': 'Tellect LMS Support API',
            'status': 'active',
            'endpoints': {
                'tickets': 'tickets/',
                'ticket_detail': 'tickets/<id>/',
                'reply': 'tickets/<id>/reply/',
            },
        })


class TicketListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == 'ADMIN':
            tickets = SupportTicket.objects.all()
        else:
            tickets = SupportTicket.objects.filter(user=request.user)
        return Response(SupportTicketSerializer(tickets, many=True).data)

    def post(self, request):
        serializer = SupportTicketCreateSerializer(data=request.data)
        if serializer.is_valid():
            ticket = serializer.save(user=request.user)
            return Response(SupportTicketSerializer(ticket).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_ticket(self, request, pk):
        try:
            ticket = SupportTicket.objects.get(pk=pk)
        except SupportTicket.DoesNotExist:
            return None
        if ticket.user != request.user and request.user.role != 'ADMIN':
            return 'forbidden'
        return ticket

    def get(self, request, pk):
        ticket = self._get_ticket(request, pk)
        if ticket == 'forbidden':
            return Response({'error': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
        if not ticket:
            return Response({'error': 'Ticket not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(SupportTicketSerializer(ticket).data)

    def patch(self, request, pk):
        if request.user.role != 'ADMIN':
            return Response({'error': 'Admin access required.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            ticket = SupportTicket.objects.get(pk=pk)
        except SupportTicket.DoesNotExist:
            return Response({'error': 'Ticket not found.'}, status=status.HTTP_404_NOT_FOUND)

        allowed = {'status', 'priority'}
        for field in allowed:
            if field in request.data:
                setattr(ticket, field, request.data[field])
        ticket.save()
        return Response(SupportTicketSerializer(ticket).data)


class TicketReplyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            ticket = SupportTicket.objects.get(pk=pk)
        except SupportTicket.DoesNotExist:
            return Response({'error': 'Ticket not found.'}, status=status.HTTP_404_NOT_FOUND)

        is_admin = request.user.role == 'ADMIN'
        if ticket.user != request.user and not is_admin:
            return Response({'error': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = TicketReplyCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        reply = TicketReply.objects.create(
            ticket=ticket,
            sender=request.user,
            message=serializer.validated_data['message'],
            is_staff_reply=is_admin,
        )
        if is_admin and ticket.status == 'open':
            ticket.status = 'in_progress'
            ticket.save()

        return Response(TicketReplySerializer(reply).data, status=status.HTTP_201_CREATED)
