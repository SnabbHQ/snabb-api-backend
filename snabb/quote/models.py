# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from datetime import datetime, timedelta
from django.utils.dateformat import format
from django.contrib.auth.models import User
from snabb.size.models import Size, MinimumPrice
from snabb.geo_utils.utils import _check_distance_between_points


class Quote(models.Model):
    quote_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    quote_user = models.ForeignKey(
        User, related_name='quote_user',
        null=True, blank=True
    )
    expire_at = models.IntegerField(default=0, editable=False, blank=True)
    tasks = models.ManyToManyField('quote.Task')
    active = models.BooleanField(default=True)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    @property
    def distance(self):
        'Returns sumatory of distance between all tasks'
        tasks = self.tasks.all().order_by('order')
        origin_task = tasks[:1][0]  # Get only the origin task
        origin_latitude = ""
        origin_longitude = ""
        distance = 0  # initialize distance
        for task in tasks:
            if origin_latitude == "" and origin_longitude == "":
                origin_latitude = task.task_place.place_address.latitude
                origin_longitude = task.task_place.place_address.longitude
            else:
                current_latitude = task.task_place.place_address.latitude
                current_longitude = task.task_place.place_address.longitude
                distance = distance + _check_distance_between_points(
                    origin_latitude,
                    origin_longitude,
                    current_latitude,
                    current_longitude
                    )
                origin_latitude = current_latitude
                origin_longitude = current_longitude
        return distance

    @property
    def prices(self):
        'Returns dictionary of size/prices'
        tasks = self.tasks.all().order_by('order')
        price_small = 0
        price_medium = 0
        price_big = 0
        eta_small = 0
        eta_medium = 0
        eta_big = 0
        data_prices = {}

        try:
            '''
            Get origin info: currency, prices, lat/lon
            '''
            task = tasks[:1][0]  # Get only the origin task
            # Get price/meter by size/city of origin.
            price_small += Size.objects.filter(
                size='small',
                size_city=task.task_place.place_address.address_city
            ).first().size_price
            price_medium += Size.objects.filter(
                size='medium',
                size_city=task.task_place.place_address.address_city
            ).first().size_price
            price_big += Size.objects.filter(
                size='big',
                size_city=task.task_place.place_address.address_city
            ).first().size_price

            # Get Minimum prices for this city.
            try:
                minimum_price_small = MinimumPrice.objects.get(
                    size='small',
                    price_city=task.task_place.place_address.address_city
                )
                minimum_price_small_meters = minimum_price_small.price_meters
                minimum_price_small_value = minimum_price_small.price_value
            except MinimumPrice.DoesNotExist:
                minimum_price_small_meters = None
                minimum_price_small_value = None

            try:
                minimum_price_medium = MinimumPrice.objects.get(
                    size='medium',
                    price_city=task.task_place.place_address.address_city
                )
                minimum_price_medium_meters = minimum_price_medium.price_meters
                minimum_price_medium_value = minimum_price_medium.price_value
            except MinimumPrice.DoesNotExist:
                minimum_price_medium_meters = None
                minimum_price_medium_value = None

            try:
                minimum_price_big = MinimumPrice.objects.get(
                    size='big',
                    price_city=task.task_place.place_address.address_city
                )
                minimum_price_big_meters = minimum_price_big.price_meters
                minimum_price_big_value = minimum_price_big.price_value
            except MinimumPrice.DoesNotExist:
                minimum_price_big_meters = None
                minimum_price_big_value = None

            distance = self.distance

            # Calculate price_small:
            if minimum_price_small_value:
                if distance < minimum_price_small_meters:
                    # Minimum Price.
                    price_small = minimum_price_small_value
                else:
                    extra_distance = distance - minimum_price_small_meters
                    base_price = minimum_price_small_value
                    extra_price = float(price_small)*extra_distance
                    price_small = base_price + extra_price
            else:
                price_small = float(price_small)*distance

            # Calculate price_medium:
            if minimum_price_medium_value:
                if distance < minimum_price_medium_meters:
                    # Minimum Price.
                    price_medium = minimum_price_medium_value
                else:
                    extra_distance = distance - minimum_price_medium_meters
                    base_price = minimum_price_medium_value
                    extra_price = float(price_medium)*extra_distance
                    price_medium = base_price + extra_price
            else:
                price_medium = float(price_medium)*distance

            # Calculate price_big:
            if minimum_price_big_value:
                if distance < minimum_price_big_meters:
                    # Minimum Price.
                    price_big = minimum_price_big_value
                else:
                    extra_distance = distance - minimum_price_big_meters
                    base_price = minimum_price_big_value
                    extra_price = float(price_big)*extra_distance
                    price_big = base_price + extra_price
            else:
                price_big = float(price_big)*distance

            # TO DO, get special price for city.
            data_prices = {
                'small': {
                    'price': price_small,
                    'eta': int(eta_small)
                },
                'medium': {
                    'price': price_medium,
                    'eta': int(eta_medium)
                },
                'big': {
                    'price': price_big,
                    'eta': int(eta_big)
                }
            }
            return data_prices
        except Exception as error:
            print(error)
            pass
            # print(error)
        return data_prices

    def __str__(self):
        return str(self.quote_id)

    class Meta:
        verbose_name = u'Quote'
        verbose_name_plural = u'Quotes'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.quote_id:
            self.created_at = int(format(datetime.now(), u'U'))
            self.expire_at = int(format(datetime.now() + timedelta(minutes=10), u'U'))
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
        default=0, blank=True
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
            self.expire_at = self.created_at + 600
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
