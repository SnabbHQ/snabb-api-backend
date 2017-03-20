from django.contrib import admin
from snabb.deliveries.models import Delivery


class DeliveryAdmin(admin.ModelAdmin):
    model = Delivery
    list_display = [
        'delivery_id', 'courier', 'delivery_quote', 'price',
        'status'
    ]

    list_filter = ['status']



admin.site.register(Delivery, DeliveryAdmin)
