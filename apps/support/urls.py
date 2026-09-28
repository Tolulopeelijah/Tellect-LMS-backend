from django.urls import path
from .views import SupportHomeView, TicketListView, TicketDetailView, TicketReplyView

urlpatterns = [
    path('', SupportHomeView.as_view(), name='support-home'),
    path('tickets/', TicketListView.as_view(), name='support-ticket-list'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='support-ticket-detail'),
    path('tickets/<int:pk>/reply/', TicketReplyView.as_view(), name='support-ticket-reply'),
]
