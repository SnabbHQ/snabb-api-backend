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
    tasks = models.ManyToManyField('quote.Task')
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
        '''price = price_pickup + price_dropoff + eta
        return price'''
        return 0

    @property
    def prices(self):
        'Returns dictionary of size/prices'
        '''pickup = Pickup.objects.filter(pickup_quote=self).first()
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
        return data_prices'''
        return 0

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


class Task(models.Model):
    TaskTypeChoices = (
        ('pickup', 'Pickup'),
        ('dropoff', 'Dropoff')
    )
    task_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    task_place = models.ForeignKey(
        'quote.Place', related_name='task_place',
        null=True, blank=True
    )
    task_contact = models.ForeignKey(
        'contact.Contact', related_name='task_contact',
        null=True, blank=True
    )
    order = models.IntegerField(
        default=0, editable=False, blank=True
    )
    comments = models.CharField(
        verbose_name="Comments", max_length=500, null=True, blank=True
    )
    task_type = models.CharField(
        verbose_name="Task Type", max_length=300, null=True, blank=True,
        choices=TaskTypeChoices
    )
    active = models.BooleanField(default=True)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return str(self.task_id)

    class Meta:
        verbose_name = u'Task'
        verbose_name_plural = u'Tasks'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.task_id:
            self.created_at = int(format(datetime.now(), u'U'))

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(Task, self).save(*args, **kwargs)


class Place(models.Model):
    place_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    place_address = models.ForeignKey(
        'address.Address', related_name='place_address',
        null=True, blank=True
    )
    description = models.CharField(
        verbose_name="Description", max_length=500, null=True, blank=True
    )
    active = models.BooleanField(default=True)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return str(self.place_id)

    class Meta:
        verbose_name = u'Place'
        verbose_name_plural = u'Places'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.place_id:
            self.created_at = int(format(datetime.now(), u'U'))

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(Place, self).save(*args, **kwargs)
