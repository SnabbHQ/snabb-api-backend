# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from datetime import datetime
from django.utils.dateformat import format
from snabb.users.models import Profile


class Quote(models.Model):
    quote_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    quote_user = models.ForeignKey(
        Profile, related_name='Quote_User',
        null=True, blank=True
    )
    active = models.BooleanField(default=True)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    @property
    def prices(self):
        'returns dictionary of size/prices'
        return {}

    @property
    def pickups(self):
        'returns pickups'
        return {}

    @property
    def dropoffs(self):
        'returns dropoffs'
        return {}

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


class Pickup(models.Model):
    pickup_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    pickup_quote = models.ForeignKey(
        'quote.Quote', related_name='pickup_quote',
        null=True, blank=True
    )
    pickup_address = models.ForeignKey(
        'address.Address', related_name='pickup_address',
        null=True, blank=True
    )
    active = models.BooleanField(default=True)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return str(self.pickup_id)

    class Meta:
        verbose_name = u'Pickup'
        verbose_name_plural = u'PickUps'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.pickup_id:
            self.created_at = int(format(datetime.now(), u'U'))

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(Pickup, self).save(*args, **kwargs)


class DropOff(models.Model):
    dropoff_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    dropoff_quote = models.ForeignKey(
        'quote.Quote', related_name='dropoff_quote',
        null=True, blank=True
    )
    dropoff_address = models.ForeignKey(
        'address.Address', related_name='dropoff_address',
        null=True, blank=True
    )
    active = models.BooleanField(default=True)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return str(self.dropoff_id)

    class Meta:
        verbose_name = u'Dropoff'
        verbose_name_plural = u'Dropoffs'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.dropoff_id:
            self.created_at = int(format(datetime.now(), u'U'))

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(DropOff, self).save(*args, **kwargs)
