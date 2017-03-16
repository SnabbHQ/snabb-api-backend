"""Models Order, for User and Courier."""
from datetime import datetime
from django.db import models
from django.utils.dateformat import format
from snabb.couriers.models import Courier
from snabb.users.models import User


class OrderUser(models.Model):
    """Model Order For User."""

    order_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    user = models.ForeignKey(
        User, related_name='BillUser', verbose_name="BillUser",
        blank=True, null=True, on_delete=models.SET_NULL
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
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=7
    )
    fee = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=7
    )
    total = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=7
    )
    updated_at = models.IntegerField(default=0, editable=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)

    def __str__(self):
        return str(self.order_id + ' - ' + self.order_reference)

    class Meta:
        verbose_name = u'Order User',
        verbose_name_plural = u'Orders User'

    def save(self, *args, **kwargs):
        """Method called on Save Model."""
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.order_id:
            self.created_at = int(format(datetime.now(), u'U'))
            # Num Factura
            prefix = 'SNABB'
            serie = 'U'
            year = str(datetime.now().year)
            orders_count = OrderUser.objects.all().count()
            num = str(orders_count+1)
            self.order_reference = prefix+'-'+year+'-'+serie+'-'+num
        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(OrderUser, self).save(*args, **kwargs)


class LineOrderUser(models.Model):
    """Model LineOrder for User."""

    line_order_user_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    order_user = models.ForeignKey(
        OrderUser, null=False,
        related_name='OrderUser', verbose_name="OrderUser"
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
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=7
    )
    discount = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=7
    )
    total = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=7
    )
    updated_at = models.IntegerField(default=0, editable=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)

    def __str__(self):
        return str(self.line_order_user_id + ' - ' + self.order_user.reference)

    class Meta:
        verbose_name = u'Line Order User',
        verbose_name_plural = u'Lines Order User'

    def save(self, *args, **kwargs):
        """Method Called on Save Model."""
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.line_order_user_id:
            self.created_at = int(format(datetime.now(), u'U'))
        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(LineOrderUser, self).save(*args, **kwargs)


class OrderCourier(models.Model):
    """Model Order For Courier."""

    order_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    courier = models.ForeignKey(
        Courier, related_name='BillCourier', verbose_name="BillCourier",
        blank=True, null=True, on_delete=models.SET_NULL
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
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=7
    )
    fee = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=7
    )
    total = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=7
    )
    updated_at = models.IntegerField(default=0, editable=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)

    def __str__(self):
        return str(self.order_id + ' - ' + self.order_reference)

    class Meta:
        verbose_name = u'Order Courier',
        verbose_name_plural = u'Orders Courier'

    def save(self, *args, **kwargs):
        """Method Called on Save Model."""
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.order_id:
            self.created_at = int(format(datetime.now(), u'U'))
            orders_count = OrderCourier.objects.all().count()
            self.order_reference = 'SNABB-2017-C-'+str(orders_count+1)
            # Falta definir Formato --> 0001

            if self.courier:
                pass

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(OrderCourier, self).save(*args, **kwargs)


class LineOrderCourier(models.Model):
    """Model LineOrder for Courier."""

    line_order_courier_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    order_courier = models.ForeignKey(
        OrderCourier, null=False,
        related_name='OrderCourier', verbose_name="OrderCourier"
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
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=7
    )
    discount = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=7
    )
    total = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=7
    )
    updated_at = models.IntegerField(default=0, editable=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)

    def __str__(self):
        return str(
            self.liner_order_courier_id + ' - ' + self.order_courier.reference
        )

    class Meta:
        verbose_name = u'Line Order Courier',
        verbose_name_plural = u'Lines Order Courier'

    def save(self, *args, **kwargs):
        """Method Called on Save Model."""
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.liner_order_courier_id:
            self.created_at = int(format(datetime.now(), u'U'))
        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(LineOrderCourier, self).save(*args, **kwargs)
