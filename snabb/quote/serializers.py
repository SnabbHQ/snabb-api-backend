from rest_framework import serializers
from .models import Quote, Pickup, DropOff
from snabb.address.serializers import AddressSerializer
from snabb.contact.serializers import ContactSerializer


class PickupSerializer(serializers.ModelSerializer):

    address = serializers.SerializerMethodField('address_info')
    contact = serializers.SerializerMethodField('contact_info')

    def address_info(self, obj):
        if obj.pickup_address:
            items = obj.pickup_address
            serializer = AddressSerializer(
                items, many=False, read_only=True
            )
            return serializer.data
        else:
            return None

    def contact_info(self, obj):
        if obj.pickup_contact:
            items = obj.pickup_contact
            serializer = ContactSerializer(
                items, many=False, read_only=True
            )
            return serializer.data
        else:
            return None

    class Meta:
        model = Pickup
        fields = (
            'pickup_id',
            'active',
            'created_at', 'updated_at',
            'contact',
            'address'
        )


class DropoffSerializer(serializers.ModelSerializer):

    address = serializers.SerializerMethodField('address_info')
    contact = serializers.SerializerMethodField('contact_info')

    def address_info(self, obj):
        if obj.dropoff_address:
            items = obj.dropoff_address
            serializer = AddressSerializer(
                items, many=False, read_only=True
            )
            return serializer.data
        else:
            return None

    def contact_info(self, obj):
        if obj.dropoff_contact:
            items = obj.dropoff_contact
            serializer = ContactSerializer(
                items, many=False, read_only=True
            )
            return serializer.data
        else:
            return None

    class Meta:
        model = DropOff
        fields = (
            'dropoff_id',
            'active',
            'created_at', 'updated_at',
            'contact',
            'address'
        )


class QuoteSerializer(serializers.ModelSerializer):

    pickup = serializers.SerializerMethodField('pickup_info')
    dropoff = serializers.SerializerMethodField('dropoff_info')

    def pickup_info(self, obj):
        if obj.pickups.count() > 0:
            items = obj.pickups.first()
            serializer = PickupSerializer(
                items, many=False, read_only=True
            )
            return serializer.data
        else:
            return None

    def dropoff_info(self, obj):
        if obj.dropoffs.count() > 0:
            items = obj.dropoffs.first()
            serializer = DropoffSerializer(
                items, many=False, read_only=True
            )
            return serializer.data
        else:
            return None

    class Meta:
        model = Quote
        fields = (
            'quote_id',
            'quote_user',
            'pickup', 'dropoff',
            'prices',
            'created_at', 'updated_at'
        )
