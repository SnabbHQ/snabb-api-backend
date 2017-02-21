# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from datetime import datetime
from django.utils.dateformat import format


class Size(models.Model):
    SizeChoices = (
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('big', 'Big')
    )
    size_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    size = models.CharField(
        verbose_name="Size type",
        max_length=50,
        null=True, blank=True,
        choices=SizeChoices
    )
    size_city = models.ForeignKey(
        'location.City', related_name='City',
        null=True, blank=True
    )
    size_price = models.DecimalField(
        verbose_name="Price/meter",
        max_digits=50, decimal_places=3, default=0.000,
        blank=True
    )

    active = models.BooleanField(default=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return '%s %s' % (self.size, self.size_city)

    class Meta:
        verbose_name = u'Size'
        verbose_name_plural = u'Sizes'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.size_id:
            self.created_at = int(format(datetime.now(), u'U'))

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(Size, self).save(*args, **kwargs)


class MinimumPrice(models.Model):
    SizeChoices = (
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('big', 'Big')
    )
    price_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    size = models.CharField(
        verbose_name="Size type",
        max_length=50,
        null=True, blank=True,
        choices=SizeChoices
    )
    price_city = models.ForeignKey(
        'location.City', related_name='price_city',
        null=True, blank=True
    )
    price_value = models.DecimalField(
        verbose_name="Minimum Price",
        max_digits=50, decimal_places=3, default=0.000,
        blank=True
    )
    price_meters = models.IntegerField(
        verbose_name="Meters",
        default=0,
        blank=True
    )
    active = models.BooleanField(default=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return '%s %s' % (self.size, self.price_city)

    class Meta:
        verbose_name = u'Minimum Price'
        verbose_name_plural = u'Minimum Prices'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.price_id:
            self.created_at = int(format(datetime.now(), u'U'))

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(MinimumPrice, self).save(*args, **kwargs)
