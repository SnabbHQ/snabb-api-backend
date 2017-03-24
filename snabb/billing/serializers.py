from rest_framework import serializers
from .models import (
    OrderUser, LineOrderUser,
    OrderCourier, LineOrderCourier
)


class OrderUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderUser
        fields = (
            'order_id', 'user', 'order_delivery', 'order_reference'
        )

class OrderCourierSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderCourier
        fields = (
            'order_id', 'courier', 'order_delivery', 'order_reference'
        )
