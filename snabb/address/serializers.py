from rest_framework import serializers
from .models import Address
from snabb.location.models import Zipcode
from snabb.location.serializers import ZipcodeSerializer


class AddressSerializer(serializers.ModelSerializer):

    zipcode = serializers.SerializerMethodField('zipcode_info')

    def zipcode_info(self, obj):
        if obj.zipcode and obj.address_city:
            try:
                zipcode_city = Zipcode.objects.get(
                    zipcode_city=obj.address_city,
                    code=obj.zipcode
                )
                return zipcode_city.code
            except Exception as error:
                return None
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
            'address_city'
        )
