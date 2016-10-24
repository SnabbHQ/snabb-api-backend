# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Delivery(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    currency_code = models.CharField(max_length=100, blank=True, default='SEK')
    owner = models.ForeignKey('auth.User', related_name='deliveries', default='')
    tracking_url = models.TextField(default='')

    class Meta:
        ordering = ('created',)
