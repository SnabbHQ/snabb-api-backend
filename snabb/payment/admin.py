from django.contrib import admin
from snabb.payment.models import Payment, Card


class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = [
        'payment_id', 'payment_user', 'amount', 'status',
        'updated_at', 'created_at'
    ]

    list_filter = ['payment_id', 'payment_user', 'status']

class CardAdmin(admin.ModelAdmin):
    model = Card
    list_display = [
        'card_id', 'user_id', 'fingerprint', 'default_card',
        'updated_at', 'created_at'
    ]

    list_filter = ['card_id', 'user_id', 'fingerprint']


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Card, CardAdmin)
