# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from datetime import datetime
from django.utils.dateformat import format


class Currency(models.Model):
    currency_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    currency = models.CharField(
        verbose_name=u'Currency',
        max_length=50,
        null=True, blank=True
    )
    symbol = models.CharField(
        verbose_name=u'Symbol',
        max_length=10,
        null=True, blank=True
    )
    active = models.BooleanField(default=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        if self.currency:
            return str(self.currency)
        return str(self.currency_id)

    class Meta:
        verbose_name = u'Currency'
        verbose_name_plural = u'Currencies'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.currency_id:
            self.created_at = int(format(datetime.now(), u'U'))

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(Currency, self).save(*args, **kwargs)
