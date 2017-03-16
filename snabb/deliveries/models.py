"""App Delivery."""
from __future__ import unicode_literals
from datetime import datetime
from django.utils.dateformat import format
from django.db import models
from snabb.billing.models import OrderCourier


class Delivery(models.Model):
    """Model Delivery."""

    statusChoices = (
        ('new', 'new'),
        ('processing', 'processing'),
        ('no_couriers_available', 'no_couriers_available'),
        ('en_route_to_pickup', 'en_route_to_pickup'),
        ('en_route_to_dropoff', 'en_route_to_dropoff'),
        ('at_dropoff', 'at_dropoff'),
        ('completed', 'completed'),
        ('unable_to_deliver', 'unable_to_deliver'),
        ('scheduled', 'scheduled'),
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
    # This would be a foreignKey to order, for now, charfield for dev,
    order_reference_id = models.CharField(
        verbose_name="Order reference",
        max_length=300,
        null=False,
        blank=True,
        default=''
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
                    order.courier = self.courier
                    order.save()
                    print ('NEW ORDER')

        super(Delivery, self).save(*args, **kwargs)
