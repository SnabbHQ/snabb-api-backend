from rest_framework import serializers
from .models import Zipcode, City, Region, Country
from snabb.currency.serializers import CurrencySerializer


class RegionSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField('country_info')

    def country_info(self, obj):
        if obj.region_country:
            items = obj.region_country
            serializer = CountrySerializer(
                items, many=False, read_only=True
            )
            return serializer.data
        else:
            return None

    class Meta:
        model = Region
        fields = (
            'name',
            'country'
        )


class ZipcodeSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField('city_info')

    def city_info(self, obj):
        if obj.zipcode_city:
            items = obj.zipcode_city
            serializer = CitySerializer(
                items, many=False, read_only=True
            )
            return serializer.data
        else:
            return None

    class Meta:
        model = Zipcode
        fields = (
            'code',
            'city'
        )


class CitySerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField('region_info')

    def region_info(self, obj):
        if obj.city_region:
            items = obj.city_region
            serializer = RegionSerializer(
                items, many=False, read_only=True
            )
            return serializer.data
        else:
            return None

    class Meta:
        model = City
        fields = (
            'name',
            'region'
        )


class CountrySerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField('currency_info')

    def currency_info(self, obj):
        if obj.country_currency:
            items = obj.country_currency
            serializer = CurrencySerializer(
                items, many=False, read_only=True
            )
            return serializer.data
        else:
            return None

    class Meta:
        model = Country
        fields = (
            'name',
            'iso_code',
            'currency'
        )
