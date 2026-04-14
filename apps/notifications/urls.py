from django.urls import path
from .views import NotificationsHomeView


urlpatterns = [
    path("", NotificationsHomeView.as_view(), name="notifications-home"),
]

