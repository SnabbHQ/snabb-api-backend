"""Register Models in Admin Panel."""
from django.contrib import admin
from snabb.billing.models import(
    OrderUser, LineOrderUser,
    OrderCourier, LineOrderCourier
)

admin.site.register(OrderUser)
admin.site.register(LineOrderUser)
admin.site.register(OrderCourier)
admin.site.register(LineOrderCourier)
