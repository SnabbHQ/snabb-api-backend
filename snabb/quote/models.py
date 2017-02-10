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

    def calculate_eta(self, address_pickup, address_dropoff, size):
        if size == 'small':
            return 10
        if size == 'medium':
            return 20
        if size == 'big':
            return 30
        return 0

    def calculate_price(self, price_pickup, price_dropoff, eta):
        price = price_pickup + price_dropoff + eta
        return price

    @property
    def prices(self):
        'Returns dictionary of size/prices'
        pickup = Pickup.objects.filter(pickup_quote=self).first()
        dropoff = DropOff.objects.filter(dropoff_quote=self).first()
        try:
            # Get Data prices from sizes
            pickup_price_small = Size.objects.filter(
                size='small',
                size_city=pickup.pickup_address.address_zipcode.zipcode_city
            ).first().size_price
            dropoff_price_small = Size.objects.filter(
                size='small',
                size_city=dropoff.dropoff_address.address_zipcode.zipcode_city
            ).first().size_price
            pickup_price_medium = Size.objects.filter(
                size='medium',
                size_city=pickup.pickup_address.address_zipcode.zipcode_city
            ).first().size_price
            dropoff_price_medium = Size.objects.filter(
                size='medium',
                size_city=dropoff.dropoff_address.address_zipcode.zipcode_city
            ).first().size_price
            pickup_price_big = Size.objects.filter(
                size='big',
                size_city=pickup.pickup_address.address_zipcode.zipcode_city
            ).first().size_price
            dropoff_price_big = Size.objects.filter(
                size='big',
                size_city=dropoff.dropoff_address.address_zipcode.zipcode_city
            ).first().size_price

            # Calculate eta pickup to dropoff - small
            eta_small = self.calculate_eta(
                pickup.pickup_address,
                dropoff.dropoff_address,
                'small'
            )
            # Calculate eta pickup to dropoff - medium
            eta_medium = self.calculate_eta(
                pickup.pickup_address,
                dropoff.dropoff_address,
                'medium'
            )
            # Calculate eta pickup to dropoff - big
            eta_big = self.calculate_eta(
                pickup.pickup_address,
                dropoff.dropoff_address,
                'big'
            )
            # Calculate price pickup to dropoff - small
            price_small = self.calculate_price(
                pickup_price_small,
                dropoff_price_small,
                eta_small
            )
            # Calculate price pickup to dropoff - medium
            price_medium = self.calculate_price(
                pickup_price_medium,
                dropoff_price_medium,
                eta_medium
            )
            # Calculate price pickup to dropoff -big
            price_big = self.calculate_price(
                pickup_price_medium,
                dropoff_price_big,
                eta_big
            )
        except Exception as error:
            print (error)
            eta_small = 0
            eta_medium = 0
            eta_big = 0
            price_small = 0
            price_medium = 0
            price_big = 0

        data_prices = {
            'size': {
                'small': {
                    'price': float(price_small),
                    'price_prio': float(price_small),
                    'eta': int(eta_small)
                },
                'medium': {
                    'price': float(price_medium),
                    'price_prio': float(price_medium),
                    'eta': int(eta_medium)
                },
                'big': {
                    'price': float(price_big),
                    'price_prio': float(price_big),
                    'eta': int(eta_big)
                }
            }
        }
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
