# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from datetime import datetime
from django.utils.dateformat import format


class Zipcode(models.Model):
    zipcode_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    code = models.IntegerField(
        verbose_name='Code', null=False
    )
    zipcode_city = models.ForeignKey(
        'location.City', related_name='Zipcode_city', null=True, blank=True
    )
    active = models.BooleanField(default=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name = u'Zipcode'
        verbose_name_plural = u'Zipcodes'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.zipcode_id:
            self.created_at = int(format(datetime.now(), u'U'))

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(Zipcode, self).save(*args, **kwargs)


class City(models.Model):
    city_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    name = models.CharField(
        verbose_name=u'City Name',
        max_length=300
    )
    city_region = models.ForeignKey(
        'location.Region', related_name='city_region',
        null=True, blank=True
    )
    active = models.BooleanField(default=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'City'
        verbose_name_plural = u'Cities'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.city_id:
            self.created_at = int(format(datetime.now(), u'U'))

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(City, self).save(*args, **kwargs)


class Region(models.Model):
    region_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    name = models.CharField(
        verbose_name=u'Region',
        max_length=300
    )
    region_country = models.ForeignKey(
        'location.Country', related_name='region_country',
        null=True, blank=True
    )
    active = models.BooleanField(default=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Region',
        verbose_name_plural = u'Regions'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.region_id:
            self.created_at = int(format(datetime.now(), u'U'))

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(Region, self).save(*args, **kwargs)


class Country(models.Model):
    country_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    name = models.CharField(
        verbose_name=u'Name Country', max_length=300
    )
    iso_code = models.CharField(
        verbose_name=u'Iso Code',
        max_length=2,
        null=True, blank=True
    )
    country_currency = models.ForeignKey(
        'currency.Currency', related_name='country_currency',
        null=True, blank=True
    )
    active = models.BooleanField(default=False)
    updated_at = models.IntegerField(default=0, editable=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Country',
        verbose_name_plural = u'Countries'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.country_id:
            self.created_at = int(format(datetime.now(), u'U'))

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(Country, self).save(*args, **kwargs)


class Address(models.Model):
    address_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    address_zip_code = models.ForeignKey(
        'location.Zipcode', related_name='Address_Zipcode',
        null=True, blank=True
    )
    address = models.CharField(
        verbose_name='Address',
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
        return str(self.address_id)

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
