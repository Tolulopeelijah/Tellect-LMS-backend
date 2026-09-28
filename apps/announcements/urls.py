from django.urls import path
from .views import AnnouncementsHomeView, AnnouncementListView, AnnouncementCreateView, AnnouncementDetailView

urlpatterns = [
    path('', AnnouncementsHomeView.as_view(), name='announcements-home'),
    path('list/', AnnouncementListView.as_view(), name='announcement-list'),
    path('create/', AnnouncementCreateView.as_view(), name='announcement-create'),
    path('<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
]
