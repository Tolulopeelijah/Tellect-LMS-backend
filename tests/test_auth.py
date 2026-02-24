from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.authentication.models import User, OTPVerification


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('auth-register')
        self.verify_url = reverse('auth-verify-otp')
        self.login_url = reverse('auth-login')

    def test_user_registration(self):
        data = {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '+2348012345678',
            'university': 'University of Lagos',
            'department': 'Computer Science',
            'level': '300',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('otp', response.data)
        self.assertIn('email', response.data)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_registration_password_mismatch(self):
        data = {
            'full_name': 'Test User',
            'email': 'test2@example.com',
            'phone_number': '+2348012345678',
            'university': 'University of Lagos',
            'department': 'Computer Science',
            'level': '300',
            'password': 'securepassword123',
            'confirm_password': 'wrongpassword',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_otp_verification(self):
        # Register first
        data = {
            'full_name': 'OTP User',
            'email': 'otp@example.com',
            'phone_number': '+2348012345678',
            'university': 'Test Uni',
            'department': 'CS',
            'level': '200',
            'password': 'testpassword123',
            'confirm_password': 'testpassword123',
        }
        reg_response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(reg_response.status_code, status.HTTP_201_CREATED)
        otp_code = reg_response.data['otp']

        # Verify OTP
        verify_data = {'email': 'otp@example.com', 'code': otp_code}
        verify_response = self.client.post(self.verify_url, verify_data, format='json')
        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', verify_response.data)
        self.assertIn('refresh', verify_response.data)

    def test_login_unverified_user(self):
        User.objects.create_user(email='unverified@example.com', password='testpass123', full_name='Unverified')
        data = {'email': 'unverified@example.com', 'password': 'testpass123'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_verified_user(self):
        user = User.objects.create_user(email='verified@example.com', password='testpass123', full_name='Verified', is_verified=True)
        data = {'email': 'verified@example.com', 'password': 'testpass123'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
