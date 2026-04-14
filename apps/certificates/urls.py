from django.urls import path
from .views import CertificatesHomeView


urlpatterns = [
    path("", CertificatesHomeView.as_view(), name="certificates-home"),
]

