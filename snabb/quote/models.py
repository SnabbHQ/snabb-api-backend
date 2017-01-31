# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from datetime import datetime
from django.utils.dateformat import format
from snabb.users.models import Profile
from snabb.location.models import Address, Zipcode
from snabb.size.models import Size


class Quote(models.Model):
    quote_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    quote_user = models.ForeignKey(
        Profile, related_name='Quote_User',
        null=True, blank=True
    )
    # FK to pickup
    # FK to dropoff
    active = models.BooleanField(default=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    @property
    def quote_prices(self):
        q = QuotePrice.objects.filter(quote=self)
        return q

    def __str__(self):
        return str(self.quote_id)

    class Meta:
        verbose_name = u'Quote'
        verbose_name_plural = u'Quotes'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.quote_id:
            self.created_at = int(format(datetime.now(), u'U'))

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(Quote, self).save(*args, **kwargs)


class QuotePrice(models.Model):
    quote_price_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    quote = models.ForeignKey(
        'quote.Quote', related_name='Quote',
        null=True, blank=True
    )
    size = models.ForeignKey(
        Size, related_name='Size',
        null=True, blank=True
    )
    price = models.FloatField(
        verbose_name='Price',
        default=0, blank=True, null=True
    )
    eta = models.IntegerField(
        default=0, blank=True, null=True
    )
    active = models.BooleanField(default=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return str(self.quote_point_id)

    class Meta:
        verbose_name = u'Quote Price'
        verbose_name_plural = u'Quote Prices'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.quote_point_id:
            self.created_at = int(format(datetime.now(), u'U'))

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(QuotePoint, self).save(*args, **kwargs)
