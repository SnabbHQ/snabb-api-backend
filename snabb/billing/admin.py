"""Register Models in Admin Panel."""
from django.contrib import admin
from snabb.billing.models import(
    ReceiptUser, LineReceiptUser,
    ReceiptCourier, LineReceiptCourier
)


class LineReceiptCourierInline(admin.StackedInline):
    model = LineReceiptCourier
    suit_classes = 'suit-tab suit-tab-lineReceiptCourier'
    extra = 0


class ReceiptCourierAdmin(admin.ModelAdmin):
    inlines = [
        LineReceiptCourierInline
    ]
    model = ReceiptCourier
    list_display = ['receipt_reference', 'total']
    readonly_fields = ('receipt_id', 'total')
    suit_form_tabs = (
        ('general', 'General'), ('lineReceiptCourier', u'Lines')
    )


class LineReceiptUserInline(admin.StackedInline):
    model = LineReceiptUser
    suit_classes = 'suit-tab suit-tab-lineReceiptUser'
    extra = 0


class ReceiptUserAdmin(admin.ModelAdmin):
    inlines = [
        LineReceiptUserInline
    ]
    model = ReceiptUser
    list_display = ['receipt_reference', 'total']
    suit_form_tabs = (
        ('general', 'General'), ('LineReceiptUser', u'Lines')
    )

admin.site.register(ReceiptCourier, ReceiptCourierAdmin)
admin.site.register(ReceiptUser, ReceiptUserAdmin)
