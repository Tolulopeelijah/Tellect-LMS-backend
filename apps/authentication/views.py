import random
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, OTPVerification
from .serializers import (
    RegisterSerializer, VerifyOTPSerializer, LoginSerializer, 
    UserProfileSerializer, PasswordResetRequestSerializer, 
    PasswordResetConfirmSerializer
)

    
class AuthHomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "name": "Tellect LMS Auth API",
            "endpoints": {
                "register": "register/",
                "verify_otp": "verify-otp/",
                "login": "login/",
                "logout": "logout/",
                "token_refresh": "token/refresh/",
                "profile": "profile/",
                "password_reset": "password/reset/",
                "password_reset_confirm": "password/reset/confirm/",
            },
        })


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            code = f'{random.randint(100000, 999999)}'
            OTPVerification.objects.filter(user=user).delete()
            OTPVerification.objects.create(user=user, code=code, is_used=False)
            return Response({
                'message': 'Registration successful. Please verify your email.',
                'email': user.email,
                'otp': code,  # Returned for testing; remove in production
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            otp = OTPVerification.objects.get(user=user)
        except OTPVerification.DoesNotExist:
            return Response({'error': 'OTP not found.'}, status=status.HTTP_400_BAD_REQUEST)

        if otp.code != code:
            return Response({'error': 'Invalid OTP code.'}, status=status.HTTP_400_BAD_REQUEST)

        if not otp.is_valid():
            return Response({'error': 'OTP has expired or already been used.'}, status=status.HTTP_400_BAD_REQUEST)

        otp.is_used = True
        otp.save()
        user.is_verified = True
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Email verified successfully.',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_verified:
            return Response({'error': 'Please verify your email before logging in.'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserProfileSerializer(user).data,
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh = RefreshToken(refresh_token)
            return Response({'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Invalid or expired refresh token.'}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                code = f'{random.randint(100000, 999999)}'
                OTPVerification.objects.filter(user=user).delete()
                OTPVerification.objects.create(user=user, code=code, is_used=False)
                # In production, send this via email
                return Response({'message': 'Password reset OTP sent to email.', 'otp': code}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'message': 'Password reset OTP sent to email.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['otp']
            try:
                user = User.objects.get(email=email)
                otp = OTPVerification.objects.get(user=user)
                
                if otp.code != code:
                    return Response({'error': 'Invalid OTP code.'}, status=status.HTTP_400_BAD_REQUEST)
                
                if not otp.is_valid():
                    return Response({'error': 'OTP has expired or already been used.'}, status=status.HTTP_400_BAD_REQUEST)
                
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                otp.is_used = True
                otp.save()
                
                return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
            except (User.DoesNotExist, OTPVerification.DoesNotExist):
                return Response({'error': 'Invalid OTP code.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

