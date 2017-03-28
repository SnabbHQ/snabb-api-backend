from rest_framework import serializers
from .models import (
    ReceiptUser, LineReceiptUser,
    ReceiptCourier, LineReceiptCourier
)


class ReceiptUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReceiptUser
        fields = (
            'receipt_id', 'user', 'receipt_delivery', 'receipt_reference'
        )

class ReceiptCourierSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReceiptCourier
        fields = (
            'receipt_id', 'courier', 'receipt_delivery', 'receipt_reference'
        )
