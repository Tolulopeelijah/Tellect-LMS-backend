from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['user', 'amount', 'status', 'created_at', 'updated_at']

class CheckoutRequestSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
