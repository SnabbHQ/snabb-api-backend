# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import time
from django.db import models


class Delivery(models.Model):
    statusChoices = (
        ('new', 'new'),
        ('processing', 'processing'),
        ('no_couriers_available', 'no_couriers_available'),
        ('en_route_to_pickup', 'en_route_to_pickup'),
        ('en_route_to_dropoff', 'en_route_to_dropoff'),
        ('at_dropoff', 'at_dropoff'),
        ('completed', 'completed'),
        ('unable_to_deliver', 'unable_to_deliver'),
        ('scheduled', 'scheduled'),
    )
    delivery_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    courier = models.ForeignKey(
        'couriers.Courier', related_name='delivery_courier',
        null=True, blank=True
    )
    price = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00
    )
    # This would be a foreignKey to order, for now, charfield for dev,
    order_reference_id = models.CharField(
        verbose_name="Order reference",
        max_length=300,
        null=False,
        blank=True,
        default=''
    )
    delivery_quote = models.ForeignKey(
        'quote.Quote', related_name='delivery_quote',
        null=True, blank=True
    )
    status = models.CharField(
        verbose_name="Status",
        max_length=300,
        null=False,
        blank=False,
        choices=statusChoices,
        default='new'
    )
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)
