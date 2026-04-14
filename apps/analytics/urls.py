from django.urls import path
from .views import AnalyticsHomeView


urlpatterns = [
    path("", AnalyticsHomeView.as_view(), name="analytics-home"),
]

