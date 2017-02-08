# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from datetime import datetime
from django.utils.dateformat import format
from django.contrib.auth.models import User
from snabb.size.models import Size


class Quote(models.Model):
    quote_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    quote_user = models.ForeignKey(
        User, related_name='quote_user',
        null=True, blank=True
    )
    active = models.BooleanField(default=True)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    @property
    def prices(self):
        'returns dictionary of size/prices'

        # Get Sizes
        pickup = Pickup.objects.filter(pickup_quote=self).first()
        dropoff = DropOff.objects.filter(dropoff_quote=self).first()
        try:
            pickup_size_small = Size.objects.filter(
                size='small',
                size_city=pickup.pickup_address.address_zip_code.zipcode_city
            ).first()
            pickup_price_small = pickup_size_small.size_price

            pickup_size_medium = Size.objects.filter(
                size='medium',
                size_city=pickup.pickup_address.address_zip_code.zipcode_city
            ).first()
            pickup_price_medium = pickup_size_medium.size_price

            pickup_size_big = Size.objects.filter(
                size='big',
                size_city=pickup.pickup_address.address_zip_code.zipcode_city
            ).first()
            pickup_price_big = pickup_size_big.size_price
        except:
            pickup_size_small = 0
            pickup_price_small = 0
            pickup_size_medium = 0
            pickup_price_medium = 0
            pickup_size_big = 0
            pickup_price_big = 0

        try:
            dropoff_size_small = Size.objects.filter(
                size='small',
                size_city=dropoff.dropoff_address.address_zip_code.zipcode_city
            ).first()
            dropoff_price_small = dropoff_size_small.size_price

            dropoff_size_medium = Size.objects.filter(
                size='medium',
                size_city=dropoff.dropoff_address.address_zip_code.zipcode_city
            ).first()
            dropoff_price_medium = dropoff_size_medium.size_price

            dropoff_size_big = Size.objects.filter(
                size='big',
                size_city=dropoff.dropoff_address.address_zip_code.zipcode_city
            ).first()
            dropoff_price_big = dropoff_size_big.size_price
        except:
            dropoff_size_small = 0
            dropoff_price_small = 0
            dropoff_size_medium = 0
            dropoff_price_medium = 0
            dropoff_size_big = 0
            dropoff_price_big = 0

        data_prices = {
            'pickup': str(pickup),
            'pickup_prices': {
                'small': float(pickup_price_small),
                'medium': float(pickup_price_medium),
                'big': float(pickup_price_big)
            },
            'dropoff': str(dropoff),
            'dropoff_prices': {
                'small': float(dropoff_price_small),
                'medium': float(dropoff_price_medium),
                'big': float(dropoff_price_big)
            }
        }
        # print (data_prices)

        return data_prices

    @property
    def pickups(self):
        'returns pickups'
        pickups = Pickup.objects.filter(pickup_quote=self)
        return pickups

    @property
    def dropoffs(self):
        'returns dropoffs'
        dropoffs = DropOff.objects.filter(dropoff_quote=self)
        return dropoffs

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
    pickup_contact = models.ForeignKey(
        'contact.Contact', related_name='pickup_contact',
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
    dropoff_contact = models.ForeignKey(
        'contact.Contact', related_name='dropoff_contact',
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
