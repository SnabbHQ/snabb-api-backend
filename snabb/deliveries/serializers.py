from rest_framework import serializers

from snabb.deliveries.models import Delivery


class DeliverySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Delivery
        fields = ('id', 'quote_id', 'currency_code', 'owner', 'tracking_url')
