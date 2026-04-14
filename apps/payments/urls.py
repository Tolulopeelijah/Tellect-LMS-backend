from django.urls import path
from .views import CheckoutView, PaystackWebhookView, TransactionHistoryView

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('webhook/paystack/', PaystackWebhookView.as_view(), name='paystack-webhook'),
    path('history/', TransactionHistoryView.as_view(), name='transaction-history'),
]
