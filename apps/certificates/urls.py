from django.urls import path
from .views import (
    CertificatesHomeView,
    MyCertificatesView,
    GenerateCertificateView,
    CertificateDetailView,
    VerifyCertificateView,
    RevokeCertificateView,
)

urlpatterns = [
    path('', CertificatesHomeView.as_view(), name='certificates-home'),
    path('my/', MyCertificatesView.as_view(), name='certificates-my'),
    path('generate/', GenerateCertificateView.as_view(), name='certificates-generate'),
    path('verify/<str:code>/', VerifyCertificateView.as_view(), name='certificates-verify'),
    path('<int:pk>/revoke/', RevokeCertificateView.as_view(), name='certificates-revoke'),
    path('<int:pk>/', CertificateDetailView.as_view(), name='certificates-detail'),
]
