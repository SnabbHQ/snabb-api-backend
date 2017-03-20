"""Register Models in Admin Panel."""
from django.contrib import admin
from snabb.billing.models import(
    OrderUser, LineOrderUser,
    OrderCourier, LineOrderCourier
)


class LineOrderCourierInline(admin.StackedInline):
    model = LineOrderCourier
    suit_classes = 'suit-tab suit-tab-lineOrderCourier'
    extra = 0


class OrderCourierAdmin(admin.ModelAdmin):
    inlines = [
        LineOrderCourierInline
    ]
    model = OrderCourier
    list_display = ['order_reference', 'total']
    readonly_fields = ('order_id', 'total')
    suit_form_tabs = (
        ('general', 'General'), ('lineOrderCourier', u'Lines')
    )


class LineOrderUserInline(admin.StackedInline):
    model = LineOrderUser
    suit_classes = 'suit-tab suit-tab-lineOrderUser'
    extra = 0


class OrderUserAdmin(admin.ModelAdmin):
    inlines = [
        LineOrderUserInline
    ]
    model = OrderUser
    list_display = ['order_reference', 'total']
    readonly_fields = ('order_id', 'total')
    suit_form_tabs = (
        ('general', 'General'), ('LineOrderUser', u'Lines')
    )

admin.site.register(OrderCourier, OrderCourierAdmin)
admin.site.register(OrderUser, OrderUserAdmin)
