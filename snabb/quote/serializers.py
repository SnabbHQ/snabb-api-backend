from rest_framework import serializers
from .models import Quote
from snabb.address.serializers import AddressSerializer
from snabb.contact.serializers import ContactSerializer


class QuoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quote
        fields = (
            'quote_id',
            'quote_user',
            'prices',
            'created_at', 'updated_at'
        )
