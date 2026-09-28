from django.urls import path
from .views import (
    NotificationsHomeView,
    NotificationListView,
    UnreadCountView,
    MarkNotificationReadView,
    MarkAllReadView,
    NotificationDeleteView,
)

urlpatterns = [
    path('', NotificationsHomeView.as_view(), name='notifications-home'),
    path('list/', NotificationListView.as_view(), name='notification-list'),
    path('unread-count/', UnreadCountView.as_view(), name='notification-unread-count'),
    path('<int:pk>/read/', MarkNotificationReadView.as_view(), name='notification-mark-read'),
    path('read-all/', MarkAllReadView.as_view(), name='notification-mark-all-read'),
    path('<int:pk>/', NotificationDeleteView.as_view(), name='notification-delete'),
]
