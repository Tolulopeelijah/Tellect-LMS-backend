import hmac
import hashlib
import json
import uuid
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from decouple import config
import requests
from apps.courses.models import Course, CourseEnrollment
from .models import Transaction
from .serializers import CheckoutRequestSerializer, TransactionSerializer

PAYSTACK_SECRET_KEY = config('PAYSTACK_SECRET_KEY', default='sk_test_mocked')

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(id=serializer.validated_data['course_id'], is_active=True)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        if CourseEnrollment.objects.filter(student=request.user, course=course).exists():
            return Response({'message': 'Already enrolled'}, status=status.HTTP_400_BAD_REQUEST)

        # Mock generating a reference and initializing transaction
        reference = f"PS_{uuid.uuid4().hex[:12].upper()}"
        amount = course.price

        transaction = Transaction.objects.create(
            user=request.user,
            course=course,
            amount=amount,
            reference=reference,
            gateway='PAYSTACK',
            status='PENDING'
        )

        amount_in_kobo = int(amount * 100)
        
        # In a real implementation we would make a POST to Paystack API
        # E.g., https://api.paystack.co/transaction/initialize
        # We'll return mock checkout details for MVP so the frontend can redirect
        checkout_url_mock = f"https://checkout.paystack.com/{reference}"

        return Response({
            'message': 'Checkout initiated',
            'checkout_url': checkout_url_mock,
            'reference': reference,
            'amount': amount,
        }, status=status.HTTP_200_OK)

class PaystackWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        payload = request.body
        signature = request.headers.get('x-paystack-signature')

        if not signature:
            return Response({'error': 'Missing signature'}, status=status.HTTP_400_BAD_REQUEST)

        # NFR-13: Webhook Signature Verification
        hash_check = hmac.new(PAYSTACK_SECRET_KEY.encode('utf-8'), payload, hashlib.sha512).hexdigest()
        if hash_check != signature:
            # If default key is used, let's bypass for local testing if explicitly needed, but standard is strictly reject
            return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

        event_data = json.loads(payload)
        event = event_data.get('event')
        
        if event == 'charge.success':
            data = event_data.get('data', {})
            reference = data.get('reference')
            try:
                transaction = Transaction.objects.get(reference=reference)
                if transaction.status != 'SUCCESS':
                    transaction.status = 'SUCCESS'
                    transaction.save()
                    
                    # Enroll user
                    CourseEnrollment.objects.get_or_create(student=transaction.user, course=transaction.course)
                    
            except Transaction.DoesNotExist:
                pass
                
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
