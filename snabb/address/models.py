# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from datetime import datetime
from django.utils.dateformat import format
from snabb.location.models import City
from django.contrib.auth.models import User
from django.contrib.gis.db import models


class Address(models.Model):
    address_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    address_city = models.ForeignKey(
        City, related_name='Address_City',
        null=True, blank=True
    )
    address = models.CharField(
        verbose_name='Address',
        max_length=300, null=True, blank=True
    )
    zipcode = models.CharField(
        verbose_name='Zipcode',
        max_length=300, null=True, blank=True
    )
    latitude = models.DecimalField(
        verbose_name=u'Latitude',
        max_digits=11, decimal_places=8,
        blank=True, null=True
    )
    longitude = models.DecimalField(
        verbose_name=u'Longitude',
        max_digits=11, decimal_places=8,
        blank=True, null=True
    )
    active = models.BooleanField(default=False)
    updated_at = models.IntegerField(default=0, editable=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)

    def __str__(self):
        if not self.zipcode and not self.address:
            return '%s' % (self.address_id)
        return '%s %s' % (self.zipcode, self.address)

    class Meta:
        verbose_name = u'Address',
        verbose_name_plural = u'Addresses'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.address_id:
            self.created_at = int(format(datetime.now(), u'U'))

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(Address, self).save(*args, **kwargs)


class AddressBook(models.Model):
    address_book_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    user = models.ForeignKey(
        User, related_name='addressbook_user',
        null=True, blank=True
    )
    addresses = models.ManyToManyField(Address)

    active = models.BooleanField(default=True)
    updated_at = models.IntegerField(default=0, editable=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)

    def __str__(self):
        return str(self.address_book_id)

    class Meta:
        verbose_name = u'AddressBook',
        verbose_name_plural = u'AddressesBook'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.address_book_id:
            self.created_at = int(format(datetime.now(), u'U'))

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(AddressBook, self).save(*args, **kwargs)
