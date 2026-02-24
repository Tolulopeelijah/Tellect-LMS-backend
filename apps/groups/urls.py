from django.urls import path
from .views import GroupListView, GroupDetailView, JoinGroupView, LeaveGroupView, MembersProgressView

urlpatterns = [
    path('', GroupListView.as_view(), name='group-list'),
    path('<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('<int:pk>/join/', JoinGroupView.as_view(), name='group-join'),
    path('<int:pk>/leave/', LeaveGroupView.as_view(), name='group-leave'),
    path('<int:pk>/members-progress/', MembersProgressView.as_view(), name='group-members-progress'),
]
