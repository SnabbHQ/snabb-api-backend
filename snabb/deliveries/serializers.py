from rest_framework import serializers
from snabb.quote.models import Quote, Task, Place
from snabb.quote.serializers import QuoteSerializer, TaskSerializer
from snabb.address.serializers import AddressSerializer
from snabb.contact.serializers import ContactSerializer
from snabb.currency.serializers import CurrencySerializer
from .models import Delivery
'''
Fields to return in serializer.
- delivery_id
- courier (courier object)
    "id": "ZxK8Ygbpr1sfYgDaNURPjXKa",
    "name": "Michael Knight",
    "phone": "+34661518132",
    "onDuty": false,
    "timeLastSeen": 1486407209054,
    "imageUrl": "https://d15p8tr8p0vffz.cloudfront.net/294.png",
    "location": [
      -0.3754607,
      39.4667116
    ],
    "vehicle": {
      "id": "h3OUAyCxLrUIdIOk8930sNMf",
      "type": "BICYCLE",
      "description": null,
      "licensePlate": null,
      "color": null,
      "timeLastModified": 1482423618129
    }
- order_reference_id (reference from order)
- quote_id (Only PK)
- tasks (tasks array fromn)
'''


class DeliverySerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField('tasks_info')
    currency = serializers.SerializerMethodField('currency_info')
    courier = serializers.SerializerMethodField('courier_info')
    # order_reference_id = serializers.SerializerMethodField('order_info')
    # Pending to add quote and order relation.

    def courier_info(self, obj):
        if obj.courier:
            response = obj.courier.courier_details
            return response
        else:
            return None

    def tasks_info(self, obj):
        if obj.delivery_quote:
            if obj.delivery_quote.tasks:
                items = obj.delivery_quote.tasks
                serializer = TaskSerializer(
                    items, many=True, read_only=True)
                return serializer.data
            else:
                return None
        else:
            return None

    def currency_info(self, obj):
        if obj.delivery_quote:
            if obj.delivery_quote.tasks:
                task = obj.delivery_quote.tasks.all().order_by('order')[:1][0]
                country = task.task_place.place_address.address_city.city_region.region_country
                currency = country.country_currency
                serializer = CurrencySerializer(
                    currency, many=False, read_only=True)
                return serializer.data
            else:
                return None
        else:
            return None
        return serializer.data

    class Meta:
        model = Delivery
        fields = (
            'delivery_id',
            'currency',
            'price',
            'created_at',
            'updated_at',
            'status',
            'tasks',
            'courier'
        )
