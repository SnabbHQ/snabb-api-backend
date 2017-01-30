# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from datetime import datetime
from django.utils.dateformat import format


class Currency(models.Model):
    currency_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    currency_type = models.IntegerField(
        verbose_name='Code', null=False
    )
    currency_active = models.BooleanField(default=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return str(self.zipcode_code)

    class Meta:
        verbose_name = u'Currency'
        verbose_name_plural = u'Currencies'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.zipcode_id:
            self.created_at = int(format(datetime.now(), u'U'))

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(Currency, self).save(*args, **kwargs)
