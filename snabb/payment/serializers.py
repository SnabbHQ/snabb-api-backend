from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            'payment_id',
            'payment_user',
            'amount',
            'status',
            'created_at',
            'updated_at'
        )
