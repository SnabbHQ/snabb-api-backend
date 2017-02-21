# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from datetime import datetime
from django.utils.dateformat import format
from django.contrib.auth.models import User
from snabb.size.models import Size
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
            print('inside task')
            if origin_latitude == "" and origin_longitude == "":
                # first iteration.
                origin_latitude = task.task_place.place_address.latitude
                origin_longitude = task.task_place.place_address.longitude
                print('first time')
            else:
                print('second time')
                current_latitude = task.task_place.place_address.latitude
                current_longitude = task.task_place.place_address.longitude
                distance = distance + _check_distance_between_points(
                    origin_latitude,
                    origin_longitude,
                    current_latitude,
                    current_longitude
                    )
                print(distance)
                origin_latitude = current_latitude
                origin_longitude = current_longitude
        print(distance)
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

            distance = self.distance

            # TO DO, get special price for city.
            data_prices = {
                'small': {
                    'price': float(price_small)*distance,
                    'eta': int(eta_small)
                },
                'medium': {
                    'price': float(price_medium)*distance,
                    'eta': int(eta_medium)
                },
                'big': {
                    'price': float(price_big)*distance,
                    'eta': int(eta_big)
                }
            }
            return data_prices
        except Exception as error:
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
