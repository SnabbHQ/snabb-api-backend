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
        'location.City', related_name='Quote',
        null=True, blank=True
    )
    size_price = models.DecimalField(
        verbose_name="Price/meter",max_digits=50, decimal_places=2, default=0.00,
        blank=True)
    active = models.BooleanField(default=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return str(self.get_size_display())+' '+self.size_city.name+' '+str(self.size_price)

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
