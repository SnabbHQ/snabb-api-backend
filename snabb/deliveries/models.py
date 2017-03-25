"""App Delivery."""
from __future__ import unicode_literals
from datetime import datetime
from django.utils.dateformat import format
from django.db import models
from snabb.billing.models import OrderCourier, OrderUser
'''
new	New delivery
processing	In process. This mean the delivery is being processed and is not yet assigned to a courier * If there are no couriers available at that moment, we will stay in processing for 30 min max.
assigned	The delivery has been assigned to a courier.
in_progress	The courier is performing the delivery.
completed	The courier has completed the delivery (we don't have a distinction yet if the delivery has been done correctly or not)
expired	The delivery has expired after being 30 min in processing.
cancelled	The delivery has been cancelled (independently if the delivery has been charged or not)
'''


class Delivery(models.Model):
    """Model Delivery."""

    statusChoices = (
        ('new', 'new'),
        ('processing', 'processing'),
        ('assigned', 'assigned'),
        ('in_progress', 'in_progress'),
        ('completed', 'completed'),
        ('expired', 'expired'),
        ('cancelled', 'cancelled'),
    )
    delivery_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    courier = models.ForeignKey(
        'couriers.Courier', related_name='delivery_courier',
        null=True, blank=True
    )
    price = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=7
    )
    delivery_quote = models.ForeignKey(
        'quote.Quote', related_name='delivery_quote',
        null=True, blank=True
    )
    status = models.CharField(
        verbose_name="Status",
        max_length=300,
        null=False,
        blank=False,
        choices=statusChoices,
        default='new'
    )
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return u'%s' % (self.delivery_id)

    class Meta:
        verbose_name = u'Delivery'
        verbose_name_plural = u'Deliveries'


    def save(self, *args, **kwargs):
        """Method called on Save Model."""
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.delivery_id:
            self.created_at = int(format(datetime.now(), u'U'))
        else:
            # Generate Order when Status Change to completed
            if self.status == 'completed':
                delivery = Delivery.objects.get(pk=self.delivery_id)
                if delivery.status != 'completed':
                    order = OrderCourier()
                    order.order_delivery = self
                    order.save()
                    print ('NEW ORDER COURIER')

                    order = OrderUser()
                    order.order_delivery = self
                    order.save()
                    print ('NEW ORDER USER')

        super(Delivery, self).save(*args, **kwargs)
