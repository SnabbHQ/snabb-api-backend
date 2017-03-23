from rest_framework import serializers
from .models import Address
from snabb.location.models import Zipcode, City
from snabb.location.serializers import ZipcodeSerializer, CitySerializer


class AddressSerializer(serializers.ModelSerializer):

    zipcode = serializers.SerializerMethodField('zipcode_info')
    city = serializers.SerializerMethodField('city_info')
    #region = serializers.SerializerMethodField('region_info')
    #country = serializers.SerializerMethodField('country_info')

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

    '''def city_info(self, obj):
        if obj.address_city:
            return obj.address_city.name
        return None'''

    def city_info(self, obj):
        if obj.address_city:
            items = City.objects.get(pk=obj.address_city.city_id)
            serializer = CitySerializer(
                items, many=False, read_only=False)
            return serializer.data
        else:
            return None

    '''def region_info(self, obj):
        if obj.address_city:
            if obj.address_city.city_region:
                return obj.address_city.city_region.name
        return None

    def country_info(self, obj):
        if obj.address_city:
            if obj.address_city.city_region:
                return obj.address_city.city_region.name
        return None'''

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
