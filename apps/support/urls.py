from django.urls import path
from .views import SupportHomeView


urlpatterns = [
    path("", SupportHomeView.as_view(), name="support-home"),
]

