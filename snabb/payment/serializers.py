from rest_framework import serializers
from .models import Payment, Card

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            'payment_id',
            'payment_delivery',
            'created_at', 'updated_at'
        )

class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = (
            'card_id',
            'user_id',
            'fingerprint', 'default_card', 'card_info',
            'created_at', 'updated_at'
        )
