from rest_framework import serializers
from .models import Address
from snabb.location.serializers import ZipcodeSerializer


class AddressSerializer(serializers.ModelSerializer):

    zipcode = serializers.SerializerMethodField('zipcode_info')

    def zipcode_info(self, obj):
        if obj.address_zipcode:
            items = obj.address_zipcode
            serializer = ZipcodeSerializer(
                items, many=False, read_only=True
            )
            return serializer.data
        else:
            return None

    class Meta:
        model = Address
        fields = (
            'address_id',
            'address',
            'latitude',
            'longitude',
            'active',
            'created_at', 'updated_at',
            'zipcode'
        )
