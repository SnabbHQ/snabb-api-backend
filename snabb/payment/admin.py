from django.contrib import admin
from snabb.payment.models import Payment


class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = [
        'payment_id', 'payment_user', 'amount', 'status',
        'updated_at', 'created_at'
    ]

    list_filter = ['payment_id', 'payment_user', 'status']


admin.site.register(Payment, PaymentAdmin)
