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
        verbose_name="Quantity Type",
        max_length=50,
        null=True, blank=True,
        choices=SizeChoices
    )
    active = models.BooleanField(default=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return str(self.size_id)

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
