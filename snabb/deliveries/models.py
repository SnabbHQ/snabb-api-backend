"""App Delivery."""
from __future__ import unicode_literals
from datetime import datetime
from django.utils.dateformat import format
from django.db import models
from snabb.billing.models import ReceiptCourier, ReceiptUser
from snabb.payment.models import Payment
from snabb.users.models import Profile
from snabb.utils.utils import get_app_info
from snabb.stripe_utils.utils import *
from snabb.payment.utils import create_payment
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
    sizeChoices = (
        ('small', 'small'),
        ('medium', 'medium'),
        ('big', 'big'),
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
    # For now, we need to save this for assignment purposes.
    size = models.CharField(
        verbose_name="Size",
        max_length=300,
        null=True,
        blank=True,
        choices=sizeChoices
    )
    assigned_at = models.IntegerField(default=0, editable=False, blank=True)
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
            self.created_at = self.updated_at
            self.delivery_id = "%s" % (uuid.uuid4(),)
            # Generate new task
            from snabb.tasks.tasks import assign_delivery
            assign_delivery(self.delivery_id, schedule=10)
        else:
            old_delivery = Delivery.objects.get(pk=self.pk)
            # Update assigned_at when status is changed to assigned
            if self.status == 'assigned' and old_delivery.status == 'processing':
                self.assigned_at = self.updated_at

            # Check if status is changed to cancelled
            if self.status == 'cancelled' and old_delivery.status != 'cancelled':
                user = self.delivery_quote.quote_user
                profile = Profile.objects.get(profile_apiuser=user)
                if not profile.enterprise:  # Payment only if not is Enterprise
                    # Check 2min to status assigned
                    delay = self.updated_at - self.assigned_at
                    time_before_payment = float(
                        get_app_info('time_before_payment', 120))
                    if delay >= time_before_payment:
                        try: # Get Percentage from city
                            price_canc = self.delivery_quote.tasks.all()\
                                [:1][0].task_place.place_address.\
                                address_city.price_canceled
                            price_canc = self.price * price_canc / 100
                        except Exception as error:
                            price_canc = self.price
                        create_payment(self, price_canc)

            # Generate Receipt when Status change to Completed
            if self.status == 'completed' and old_delivery.status != 'completed':
                receipt = ReceiptCourier() # Receipt Courier
                receipt.receipt_delivery = self
                receipt.save()
                receipt = ReceiptUser() # Receipt User
                receipt.receipt_delivery = self
                receipt.save()

                if not profile.enterprise:
                    create_payment(self, self.price)

        super(Delivery, self).save(*args, **kwargs)
