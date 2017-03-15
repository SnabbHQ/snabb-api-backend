# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from datetime import datetime, timedelta
from django.utils.dateformat import format


class OrderUser(models.Model):
    """Order For User."""

    order_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    user = models.ForeignKey(
        User, null=False
        related_name='BillUser', verbose_name="BillUser",
    )
    order_reference = models.CharField(
        verbose_name="Reference",
        max_length=500, null=False,
        unique=True, editable=False
    )
    nif = models.CharField(
        verbose_name=u'NIF',
        max_length=15, null=True, blank=True
    )
    address = models.CharField(
        verbose_name=u'Address',
        max_length=100, null=True, blank=True
    )
    region = models.CharField(
        verbose_name=u'Region',
        max_length=100, null=True, blank=True
    )
    zipcode = models.CharField(
        verbose_name=u'ZipCode',
        max_length=15, null=True, blank=True
    )
    country = models.CharField(
        verbose_name=u'Country',
        max_length=50, null=True, blank=True
    )
    city = models.CharField(
        verbose_name=u'City',
        max_length=50, null=True, blank=True
    )
    tax = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00
    )
    fee = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00
    )
    total = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00
    )
    updated_at = models.IntegerField(default=0, editable=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)

    def __str__(self):
        return str(self.order_id + ' - ' + self.order_reference)

    class Meta:
        verbose_name = u'OrderUser',
        verbose_name_plural = u'OrdersUser'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.order_id:
            self.created_at = int(format(datetime.now(), u'U'))
            orders_count = OrderUser.objects.all().count()
            self.order_reference = 'SNABB-2017-U-'+str(orders_count+1)
            # Falta definir Formato --> 0001
        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(OrderUser, self).save(*args, **kwargs)


class LineOrderUser(models.Model):
    line_order_user_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    order_user = models.ForeignKey(
        OrderUser, null=False
        related_name='OrderUser', verbose_name="OrderUser",
    )
    task = models.CharField(
        verbose_name=u'Task',
        max_length=200, null=True, blank=True
    )
    description = models.CharField(
        verbose_name=u'Task',
        max_length=200, null=True, blank=True
    )
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00
    )
    discount = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00
    )
    total = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00
    )
    updated_at = models.IntegerField(default=0, editable=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)

    def __str__(self):
        return str(self.line_order_user_id + ' - ' + self.order_user.reference)

    class Meta:
        verbose_name = u'LineOrderUser',
        verbose_name_plural = u'LinesOrderUser'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.line_order_user_id:
            self.created_at = int(format(datetime.now(), u'U'))
        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(LineOrderUser, self).save(*args, **kwargs)
