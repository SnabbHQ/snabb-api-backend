# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from datetime import datetime, timedelta
from django.utils.dateformat import format
from django.contrib.auth.models import User
from snabb.size.models import Size, MinimumPrice
from snabb.geo_utils.utils import _check_distance_between_points
from snabb.dispatching.utils import (
    _get_eta,
    _create_task,
    _get_task_detail,
    _assign_task,
    _delete_task
)
import decimal
from django.db.models.signals import pre_delete
import uuid


class Quote(models.Model):
    quote_id = models.CharField(
        primary_key=True, editable=False, max_length=300, null=False,
        blank=False
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

    # TODO - This requires a big factory as currently we are doing the exact
    # same operations for three different packeges instead of applying a function
    # for each of the available package sizes.
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
        # GET ETAs
        origin_lat = str(tasks[:1][0].task_place.place_address.latitude)
        origin_lon = str(tasks[:1][0].task_place.place_address.longitude)
        pickup_etas = _get_eta(origin_lat, origin_lon)
        try:
            '''
            Get origin info: currency, prices, lat/lon
            '''
            task = tasks[:1][0]  # Get only the origin task

            # Get price/meter by size/city of origin.
            size_small = Size.objects.filter(
                size='small',
                size_city=task.task_place.place_address.address_city
            ).first()
            if size_small is not None:
                price_small = size_small.size_price

            size_medium = Size.objects.filter(
                size='medium',
                size_city=task.task_place.place_address.address_city
            ).first()
            if size_medium is not None:
                price_medium = size_medium.size_price


            size_big = Size.objects.filter(
                size='big',
                size_city=task.task_place.place_address.address_city
            ).first()
            if size_big is not None:
                price_big = size_big.size_price

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
                print(minimum_price_medium)
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
                    price_small = minimum_price_small_value
                else:
                    extra_distance = distance - minimum_price_small_meters
                    base_price = minimum_price_small_value
                    extra_price = price_small * extra_distance
                    price_small = base_price + extra_price
            else:
                price_small = price_small * distance

            # Calculate price_medium:
            if minimum_price_medium_value:
                if distance < minimum_price_medium_meters:
                    price_medium = minimum_price_medium_value
                else:
                    extra_distance = distance - minimum_price_medium_meters
                    base_price = minimum_price_medium_value
                    extra_price = price_medium * extra_distance
                    price_medium = base_price + extra_price
            else:
                price_medium = price_medium * distance

            # Calculate price_big:
            if minimum_price_big_value:
                if distance < minimum_price_big_meters:
                    price_big = minimum_price_big_value
                else:
                    extra_distance = distance - minimum_price_big_meters
                    base_price = minimum_price_big_value
                    extra_price = price_big * extra_distance
                    price_big = base_price + extra_price
            else:
                price_big = price_big * distance

            # Finally add the calculated prices to the response object
            ROUND_TO = decimal.Decimal("0.01")
            data_prices = {}

            if price_small != 0:
                data_prices['small'] = {
                    'price': price_small.quantize(ROUND_TO),
                    'eta': pickup_etas['small']
                }

            if price_medium != 0:
                data_prices['medium'] = {
                    'price': price_medium.quantize(ROUND_TO),
                    'eta': pickup_etas['medium']
                }

            if price_big != 0:
                data_prices['big'] = {
                    'price': price_big.quantize(ROUND_TO),
                    'eta': pickup_etas['big']
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
            self.quote_id = "%s" % (uuid.uuid4(),)
            self.expire_at = int(
                format(datetime.now() + timedelta(minutes=10), u'U'))
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
    task_onfleet_id = models.CharField(
        verbose_name="Onfleet ID", max_length=500, null=True, blank=True)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    @property
    def task_detail(self):
        "Returns team info from dispatching platform."
        task_details = _get_task_detail(self.task_onfleet_id)
        return task_details

    @property
    def send_dispatching(self):
        '''
        Only for testing purposes
        '''
        if not self.task_onfleet_id:
            try:
                destination = {
                    'address':
                    {"unparsed": self.task_place.place_address.address},
                    'notes': self.task_place.description
                }
                notes = self.comments
                recipients = []
                recipient = {"name": self.task_contact._get_full_name(),
                             "phone": self.task_contact.phone,
                             "notes": self.comments}
                recipients.append(recipient)

                if self.task_type == 'pickup':
                    pickupTask = True
                else:
                    pickupTask = False

                # Create task in onfleet.
                new_task = _create_task(destination, recipients,
                                        notes, pickupTask)
                return new_task
            except Exception as error:
                print(error)
                return None
        else:
            # Already exists at onfleet
            task_detail = _get_task_detail(self.task_onfleet_id)
            return task_detail

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

            # Assign to worker_id ONLY for testing purposes
            # This sould be at our assignment async worker.
            assigned_task = _assign_task(
                self.task_onfleet_id,
                'bqHwe8jkWOUA*EtimgJkS4FQ'
            )
            print (assigned_task)

        # Create in onfleet. ONLY for testing purposes
        if not self.task_onfleet_id:
            created_task = self.send_dispatching
            if created_task is not None:
                self.task_onfleet_id = self.send_dispatching['id']

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


def delete_task(sender, instance, **kwargs):
    try:
        _delete_task(instance.task_onfleet_id)
    except Exception as error:
        print(error)


pre_delete.connect(
    delete_task, sender=Task, dispatch_uid="delete_task")
