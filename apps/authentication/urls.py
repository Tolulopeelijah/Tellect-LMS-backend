from django.urls import path
from .views import (
    AuthHomeView, RegisterView, VerifyOTPView, LoginView, LogoutView, 
    TokenRefreshView, ProfileView, PasswordResetRequestView, PasswordResetConfirmView
)

urlpatterns = [
    path('', AuthHomeView.as_view(), name='auth-home'),
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='auth-verify-otp'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='auth-token-refresh'),
    path('profile/', ProfileView.as_view(), name='auth-profile'),
    path('password/reset/', PasswordResetRequestView.as_view(), name='auth-password-reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='auth-password-reset-confirm'),
]
