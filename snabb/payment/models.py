"""App Payment."""
from __future__ import unicode_literals
from datetime import datetime
from django.utils.dateformat import format
from django.db import models
from django.contrib.auth.models import User
from snabb.deliveries.models import Delivery
import uuid


class Payment(models.Model):
    """Model Payment."""
    statusChoices = (
        ('processing', 'processing'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled')
    )

    payment_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    payment_user = models.ForeignKey(
        User, related_name='payment_user',
        null=False, blank=False
    )
    payment_delivery = models.ForeignKey(
        Delivery, related_name='payment_delivery',
        null=False, blank=False
    )
    amount = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=7
    )
    currency = models.CharField(
        verbose_name="Currency",
        max_length=20, null=False, blank=False, default='eur'
    )
    description = models.CharField(
        verbose_name="Description", max_length=300, null=True, blank=True
    )
    status = models.CharField(
        verbose_name="Status", max_length=300, null=False, blank=False,
        choices=statusChoices, default='processing'
    )
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return u'%s' % (self.payment_id)

    class Meta:
        verbose_name = u'Payment'
        verbose_name_plural = u'Payments'


    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.payment_id:
            self.created_at = self.updated_at

        super(Payment, self).save(*args, **kwargs)
