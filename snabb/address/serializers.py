from rest_framework import serializers
from .models import Address
from snabb.location.serializers import ZipcodeSerializer


class AddressSerializer(serializers.ModelSerializer):

    zipcode = serializers.SerializerMethodField('zipcode_info')
    city = serializers.SerializerMethodField('city_info')

    def zipcode_info(self, obj):
        if obj.address_zipcode:
            return obj.address_zipcode.code
        else:
            return None

    def city_info(self, obj):
        if obj.address_zipcode.zipcode_city:
            return obj.address_zipcode.zipcode_city.name
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
            'zipcode',
            'city'
        )
