from django.urls import path
from .views import AnnouncementsHomeView


urlpatterns = [
    path("", AnnouncementsHomeView.as_view(), name="announcements-home"),
]

