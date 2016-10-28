from rest_framework import serializers

from snabb.deliveries.models import Delivery, Location, Quote


class DeliverySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Delivery
        fields = ('id', 'quote_id', 'currency_code', 'owner', 'tracking_url')


class QuoteSerializer(serializers.HyperlinkedModelSerializer):
    quote_id = serializers.HyperlinkedIdentityField(view_name='delivery-quote_id')

    class Meta:
        model = Quote
        fields = ('id', 'quote_id', 'currency_code', 'pickup_eta', 'delivery_eta')


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'address', 'city', 'postal_code', 'country', 'latitude', 'longitude')
