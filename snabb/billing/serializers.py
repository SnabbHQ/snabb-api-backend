from rest_framework import serializers
from .models import (
    ReceiptUser, LineReceiptUser,
    ReceiptCourier, LineReceiptCourier
)


class ReceiptUserSerializer(serializers.ModelSerializer):

    user_id = serializers.SerializerMethodField('user')
    delivery_id = serializers.SerializerMethodField('delivery')
    reference = serializers.SerializerMethodField('reference_info')

    def user(self, obj):
        return obj.user.pk
    def delivery(self, obj):
        return obj.receipt_delivery.pk
    def reference_info(self, obj):
        return obj.receipt_reference

    class Meta:
        model = ReceiptUser
        fields = (
            'receipt_id', 'user_id', 'delivery_id', 'reference'
        )

class ReceiptCourierSerializer(serializers.ModelSerializer):

    courier_id = serializers.SerializerMethodField('courier')
    delivery_id = serializers.SerializerMethodField('delivery')
    reference = serializers.SerializerMethodField('reference_info')

    def courier(self, obj):
        return obj.courier.pk
    def delivery(self, obj):
        return obj.receipt_delivery.pk
    def reference_info(self, obj):
        return obj.receipt_reference

    class Meta:
        model = ReceiptCourier
        fields = (
            'receipt_id', 'courier_id', 'delivery_id', 'reference'
        )
