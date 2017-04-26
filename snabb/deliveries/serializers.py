from rest_framework import serializers
from snabb.quote.models import Quote, Task, Place
from snabb.quote.serializers import QuoteSerializer, TaskSerializer
from snabb.address.serializers import AddressSerializer
from snabb.contact.serializers import ContactSerializer
from snabb.currency.serializers import CurrencySerializer
from snabb.billing.serializers import ReceiptUserSerializer
from .models import Delivery


class DeliverySerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField('tasks_info')
    currency = serializers.SerializerMethodField('currency_info')
    courier = serializers.SerializerMethodField('courier_info')
    delivery_receipt_id = serializers.SerializerMethodField('receipt')

    def courier_info(self, obj):
        if obj.courier:
            if self.context['action'] == 'list':
                response = obj.courier.name
            else:
                response = obj.courier.courier_details
            return response
        else:
            return None

    def tasks_info(self, obj):
        if obj.delivery_quote:
            if obj.delivery_quote.tasks:
                items = obj.delivery_quote.tasks
                serializer = TaskSerializer(
                    items, many=True, read_only=True, context=self.context)
                return serializer.data
            else:
                return None
        else:
            return None

    def currency_info(self, obj):
        if obj.delivery_quote:
            if obj.delivery_quote.tasks:
                task = obj.delivery_quote.tasks.all().order_by('order')[:1][0]
                if task.task_place.place_address.address_city.city_region is not None:
                    country = task.task_place.place_address.address_city.city_region.region_country
                    currency = country.country_currency
                    serializer = CurrencySerializer(
                        currency, many=False, read_only=True)
                    return serializer.data
                else:
                    return None
            else:
                return None
        else:
            return None
        return serializer.data

    def receipt(self, obj):
        if hasattr(obj, 'delivery_receipt'):
            items = obj.delivery_receipt
            serializer = ReceiptUserSerializer(
                items, many=False, read_only=True)
            return serializer.data
        else:
            return None

    class Meta:
        model = Delivery
        fields = (
            'delivery_id',
            'currency',
            'price',
            'created_at',
            'updated_at',
            'status',
            'courier',
            'tasks',
            'delivery_receipt_id'
        )
