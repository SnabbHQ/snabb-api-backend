"""App Payment."""
from __future__ import unicode_literals
from datetime import datetime
from django.utils.dateformat import format
from django.db import models
from django.contrib.auth.models import User
import uuid
from pinax.stripe.actions import sources, customers


class Card(models.Model):
    """Card Model."""
    card_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user_id = models.ForeignKey(
        User, related_name='card_user',
        null=False, blank=False
    )
    fingerprint = models.CharField(
        verbose_name="FingerPrint",
        max_length=250, null=False, blank=False
    )
    default_card = models.BooleanField(
        default=False, verbose_name='DefaultCard'
    )
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    @property
    def card_info(self):
        try:
            customer = customers.get_customer_for_user(user=self.user_id)
            for card in customer.stripe_customer.sources.data:
                if card.fingerprint == self.fingerprint:
                    return {
                        "id": card.id,
                        "fingerprint": card.fingerprint,
                        "customer": card.customer,
                        "exp_year": card.exp_year,
                        "exp_month": card.exp_month,
                        "last4": card.last4,
                        "brand": card.brand,
                        "funding": card.funding
                    }
            return None
        except Exception as error:
            return None

    def __str__(self):
        return u'%s' % (self.card_id)

    class Meta:
        verbose_name = u'Card'
        verbose_name_plural = u'Cards'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.card_id:
            self.created_at = self.updated_at

        super(Card, self).save(*args, **kwargs)


class Payment(models.Model):
    """Model Payment."""
    statusChoices = (
        ('processing', 'processing'),
        ('completed', 'completed'),
        ('failed', 'failed')
    )

    payment_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    payment_user = models.ForeignKey(
        User, related_name='payment_user',
        null=False, blank=False
    )
    payment_delivery = models.ForeignKey(
        'deliveries.Delivery', related_name='payment_delivery',
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
