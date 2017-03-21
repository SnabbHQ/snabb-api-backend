"""Models Order, for User and Courier."""
from datetime import datetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.dateformat import format
from snabb.couriers.models import Courier
from snabb.users.models import User, Profile
from snabb.app_info.models import AppInfo


class OrderUser(models.Model):
    """Model Order For User."""

    order_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    order_delivery = models.ForeignKey(
        'deliveries.Delivery', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='Order_User_Delivery', verbose_name="Delivery"
    )
    user = models.ForeignKey(
        User, related_name='Bill_User', verbose_name="User",
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
    name = models.CharField(
        verbose_name=u'Name',
        max_length=100, null=True, blank=True
    )
    company = models.CharField(
        verbose_name=u'Company',
        max_length=100, null=True, blank=True
    )
    phone = models.CharField(
        verbose_name=u'Phone',
        max_length=100, null=True, blank=True
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
    snabb_nif = models.CharField(
        verbose_name=u'SNABB_NIF',
        max_length=15, null=True, blank=True
    )
    snabb_name = models.CharField(
        verbose_name=u'SNABB_Name',
        max_length=100, null=True, blank=True
    )
    snabb_company = models.CharField(
        verbose_name=u'SNABB_Company',
        max_length=100, null=True, blank=True
    )
    snabb_phone = models.CharField(
        verbose_name=u'SNABB_Phone',
        max_length=100, null=True, blank=True
    )
    snabb_address = models.CharField(
        verbose_name=u'SNABB_Address',
        max_length=100, null=True, blank=True
    )
    snabb_region = models.CharField(
        verbose_name=u'SNABB_Region',
        max_length=100, null=True, blank=True
    )
    snabb_zipcode = models.CharField(
        verbose_name=u'SNABB_ZipCode',
        max_length=15, null=True, blank=True
    )
    snabb_country = models.CharField(
        verbose_name=u'SNABB_Country',
        max_length=50, null=True, blank=True
    )
    snabb_city = models.CharField(
        verbose_name=u'SNABB_City',
        max_length=50, null=True, blank=True
    )
    tax = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=7
    )
    fee = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=7
    )
    total = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=10
    )

    '''@property
    def total(self):
        lines = LineOrderUser.objects.filter(order_user=self)
        total = 0
        if lines.count() > 0:
            for line in lines:
                total += line.total
        return total
    '''

    updated_at = models.IntegerField(default=0, editable=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)

    def __str__(self):
        return str(self.order_id)

    class Meta:
        verbose_name = u'Order User',
        verbose_name_plural = u'Orders User'

    def save(self, *args, **kwargs):
        """Method called on Save Model."""
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.order_id:
            self.created_at = self.updated_at
            try:  # Num Factura
                prefix = AppInfo.objects.get(name='prefix_order_user').content
            except AppInfo.DoesNotExist:
                prefix = 'SNABB'
            try:
                prefix = AppInfo.objects.get(name='serie_order_user').content
            except AppInfo.DoesNotExist:
                serie = 'U'
            year = str(datetime.now().year)
            orders_count = OrderUser.objects.all().count()
            num = str(orders_count+1)
            self.order_reference = prefix+'-'+year+'-'+serie+'-'+num

            if self.order_delivery:
                quote = self.order_delivery.delivery_quote
                self.user = quote.quote_user

            if self.user:
                profile = Profile.objects.get(profile_apiuser=self.user)
                self.name = profile.first_name
                self.phone = profile.phone
                self.company = profile.company_name
                # Campos por rellenar:
                # self.nif = ''
                # self.address = ''
                # self.region = ''
                # self.zipcode = ''
                # self.country = ''
                # self.city = ''
                # self.tax = 0

            # Get Data from AppInfo
            try:
                self.snabb_nif = AppInfo.objects.get(name='nif').content
            except AppInfo.DoesNotExist:
                self.snabb_nif = None
            try:
                self.snabb_name = AppInfo.objects.get(name='name').content
            except AppInfo.DoesNotExist:
                self.snabb_name = None
            try:
                self.snabb_company = AppInfo.objects.get(name='company').content
            except AppInfo.DoesNotExist:
                self.snabb_company = None
            try:
                self.snabb_phone = AppInfo.objects.get(name='phone').content
            except AppInfo.DoesNotExist:
                self.snabb_phone = None
            try:
                self.snabb_address = AppInfo.objects.get(name='address').content
            except AppInfo.DoesNotExist:
                self.snabb_address = None
            try:
                self.snabb_region = AppInfo.objects.get(name='region').content
            except AppInfo.DoesNotExist:
                self.snabb_region = None
            try:
                self.snabb_zipcode = AppInfo.objects.get(name='zipcode').content
            except AppInfo.DoesNotExist:
                self.snabb_zipcode = None
            try:
                self.snabb_country = AppInfo.objects.get(name='country').content
            except AppInfo.DoesNotExist:
                self.snabb_country = None
            try:
                self.snabb_city = AppInfo.objects.get(name='city').content
            except AppInfo.DoesNotExist:
                self.snabb_city = None

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
        return str(
            str(self.line_order_user_id) + ' - ' +
            str(self.order_user.order_reference)
        )

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
        Courier, related_name='Bill_Courier', verbose_name="Courier",
        blank=True, null=True, on_delete=models.SET_NULL
    )
    order_delivery = models.ForeignKey(
        'deliveries.Delivery', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='Order_Courier_Delivery', verbose_name="Delivery"
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
    name = models.CharField(
        verbose_name=u'Name',
        max_length=100, null=True, blank=True
    )
    company = models.CharField(
        verbose_name=u'Company',
        max_length=100, null=True, blank=True
    )
    phone = models.CharField(
        verbose_name=u'Phone',
        max_length=100, null=True, blank=True
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
    snabb_nif = models.CharField(
        verbose_name=u'SNABB_NIF',
        max_length=15, null=True, blank=True
    )
    snabb_name = models.CharField(
        verbose_name=u'SNABB_Name',
        max_length=100, null=True, blank=True
    )
    snabb_company = models.CharField(
        verbose_name=u'SNABB_Company',
        max_length=100, null=True, blank=True
    )
    snabb_phone = models.CharField(
        verbose_name=u'SNABB_Phone',
        max_length=100, null=True, blank=True
    )
    snabb_address = models.CharField(
        verbose_name=u'SNABB_Address',
        max_length=100, null=True, blank=True
    )
    snabb_region = models.CharField(
        verbose_name=u'SNABB_Region',
        max_length=100, null=True, blank=True
    )
    snabb_zipcode = models.CharField(
        verbose_name=u'SNABB_ZipCode',
        max_length=15, null=True, blank=True
    )
    snabb_country = models.CharField(
        verbose_name=u'SNABB_Country',
        max_length=50, null=True, blank=True
    )
    snabb_city = models.CharField(
        verbose_name=u'SNABB_City',
        max_length=50, null=True, blank=True
    )
    tax = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=7
    )
    fee = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=7
    )
    total = models.DecimalField(
        null=False, blank=False, decimal_places=2, default=0.00, max_digits=10
    )
    '''@property
    def total(self):
        lines = LineOrderCourier.objects.filter(order_courier=self)
        total = 0
        if lines.count() > 0:
            for line in lines:
                total += line.total
        return total
    '''

    updated_at = models.IntegerField(default=0, editable=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)

    def __str__(self):
        # return str(self.order_id + ' - ' + self.order_reference)
        return str(self.order_id)

    class Meta:
        verbose_name = u'Order Courier',
        verbose_name_plural = u'Orders Courier'

    def save(self, *args, **kwargs):
        """Method Called on Save Model."""
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.order_id:
            self.created_at = int(format(datetime.now(), u'U'))

            try:  # Num Factura
                prefix = AppInfo.objects.get(name='prefix_order_courier').content
            except AppInfo.DoesNotExist:
                prefix = 'SNABB'
            try:
                prefix = AppInfo.objects.get(name='serie_order_courier').content
            except AppInfo.DoesNotExist:
                serie = 'C'

            year = str(datetime.now().year)
            orders_count = OrderCourier.objects.all().count()
            num = str(orders_count+1)
            self.order_reference = prefix+'-'+year+'-'+serie+'-'+num

            if self.order_delivery:
                self.courier = self.order_delivery.courier

            if self.courier:
                self.name = self.courier.name
                self.phone = self.courier.phone
                self.fee = self.courier.fee
                # Campos por rellenar:
                # self.nif = ''
                # self.company = ''
                # self.address = ''
                # self.region = ''
                # self.zipcode = ''
                # self.country = ''
                # self.city = ''
                # self.tax = 0

            # Get Data from AppInfo
            try:
                self.snabb_nif = AppInfo.objects.get(name='nif').content
            except AppInfo.DoesNotExist:
                self.snabb_nif = None
            try:
                self.snabb_name = AppInfo.objects.get(name='name').content
            except AppInfo.DoesNotExist:
                self.snabb_name = None
            try:
                self.snabb_company = AppInfo.objects.get(name='company').content
            except AppInfo.DoesNotExist:
                self.snabb_company = None
            try:
                self.snabb_phone = AppInfo.objects.get(name='phone').content
            except AppInfo.DoesNotExist:
                self.snabb_phone = None
            try:
                self.snabb_address = AppInfo.objects.get(name='address').content
            except AppInfo.DoesNotExist:
                self.snabb_address = None
            try:
                self.snabb_region = AppInfo.objects.get(name='region').content
            except AppInfo.DoesNotExist:
                self.snabb_region = None
            try:
                self.snabb_zipcode = AppInfo.objects.get(name='zipcode').content
            except AppInfo.DoesNotExist:
                self.snabb_zipcode = None
            try:
                self.snabb_country = AppInfo.objects.get(name='country').content
            except AppInfo.DoesNotExist:
                self.snabb_country = None
            try:
                self.snabb_city = AppInfo.objects.get(name='city').content
            except AppInfo.DoesNotExist:
                self.snabb_city = None
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
            str(self.line_order_courier_id) + ' - ' +
            str(self.order_courier.order_reference)
        )

    class Meta:
        verbose_name = u'Line Order Courier',
        verbose_name_plural = u'Lines Order Courier'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.line_order_courier_id:
            self.created_at = int(format(datetime.now(), u'U'))
        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(LineOrderCourier, self).save(*args, **kwargs)


@receiver(post_save, sender=OrderCourier)
def create_lines_order_courier(sender, instance, **kwargs):
    """Create lines for Order Courier when is created."""
    order = instance
    # Execute only when order is created
    if order.created_at == order.updated_at:
        delivery = order.order_delivery
        line = LineOrderCourier()
        line.order_courier = order
        line.price = delivery.price
        line.description = 'Delivery'
        line.task = 'Task 1'
        line.quantity = 1
        line.discount = 0
        line.total = (line.price * line.quantity) - line.discount
        line.save()
        order.updated_at += 1
        order.total = line.total
        order.save()


@receiver(post_save, sender=OrderUser)
def create_lines_order_user(sender, instance, **kwargs):
    """Create lines for Order User when is created."""
    order = instance
    # Execute only when order is created
    if order.created_at == order.updated_at:
        delivery = order.order_delivery
        line = LineOrderUser()
        line.order_user = order
        line.price = delivery.price
        line.description = 'Delivery'
        line.task = 'Task 1'
        line.quantity = 1
        line.discount = 0
        line.total = (line.price * line.quantity) - line.discount
        line.save()
        order.updated_at += 1
        order.total = line.total
        order.save()
