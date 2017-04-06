"""App Delivery."""
from __future__ import unicode_literals
from datetime import datetime
from django.utils.dateformat import format
from django.db import models
from snabb.billing.models import ReceiptCourier, ReceiptUser
from snabb.payment.models import Payment
from snabb.stripe_utils.utils import *
import uuid
import time


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
    delivery_id = models.CharField(
        primary_key=True, editable=False, max_length=300, null=False,
        blank=False
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
            self.delivery_id = "%s" % (uuid.uuid4(),)
            # Generate new task
            from snabb.tasks.tasks import assign_delivery
            now = int(format(datetime.now(), u'U'))
            assign_delivery(self.delivery_id, schedule=30)
            print ("\t[DATE] --> " + time.strftime("%c") + " <--[DATE]")
            # first iteration in 30 seg.
        else:
            # Generate Receipt when Status Change to completed
            if self.status == 'completed':
                delivery = Delivery.objects.get(pk=self.delivery_id)
                if delivery.status != 'completed':
                    # Receipt Courier
                    receipt = ReceiptCourier()
                    receipt.receipt_delivery = self
                    receipt.save()

                    # Receipt User
                    receipt = ReceiptUser()
                    receipt.receipt_delivery = self
                    receipt.save()

                    # Payment from User
                    # Get Customer
                    user = self.delivery_quote.quote_user
                    customer = get_or_create_customer(user)
                    # Get Default Card
                    card = get_default_source(customer)
                    if not card:
                        print ('DEFAULT CARD NOT EXISTS')
                    else:
                        # Generate Django Payment
                        payment = Payment()
                        payment.payment_user = user
                        payment.payment_delivery = self
                        payment.amount = Decimal(self.price)
                        payment.currency = 'eur'
                        payment.description = str(self.delivery_id)
                        payment.status = 'processing'
                        payment.save()

                        # Get Delivery price
                        data_charge = {
                            'customer': customer,
                            'card': card,
                            'amount': payment.amount,
                            'currency': payment.currency,
                            'description': payment.description
                        }
                        # Generate charge
                        if create_charge(data_charge):
                            print ('PAYMENT SUCCESSFUL')
                            payment.status = 'completed'
                        else:
                            payment.status = 'cancelled'
                        payment.save()


        super(Delivery, self).save(*args, **kwargs)
