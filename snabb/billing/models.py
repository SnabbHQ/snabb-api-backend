"""Models Receipt, for User and Courier."""
from datetime import datetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.dateformat import format
from snabb.couriers.models import Courier
from snabb.users.models import User, Profile
from snabb.utils.utils import get_app_info


class ReceiptUser(models.Model):
    """Model Receipt For User."""

    receipt_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    receipt_delivery = models.ForeignKey(
        'deliveries.Delivery', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='Receipt_User_Delivery', verbose_name="Delivery"
    )
    user = models.ForeignKey(
        User, related_name='Bill_User', verbose_name="User",
        blank=True, null=True, on_delete=models.SET_NULL
    )
    receipt_reference = models.CharField(
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
    updated_at = models.IntegerField(default=0, editable=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)

    def __str__(self):
        return str(self.receipt_id)

    class Meta:
        verbose_name = u'Receipt User',
        verbose_name_plural = u'Receipts User'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.receipt_id:
            self.created_at = self.updated_at
            prefix = get_app_info('prefix_receipt_user', 'SNABB')
            serie = get_app_info('serie_receipt_user', 'U')
            year = str(datetime.now().year)
            receipts_count = ReceiptUser.objects.all().count()
            num = str(receipts_count+1)
            self.receipt_reference = prefix+'-'+year+'-'+serie+'-'+num

            if self.receipt_delivery:
                quote = self.receipt_delivery.delivery_quote
                self.user = quote.quote_user

            if self.user:
                profile = Profile.objects.get(profile_apiuser=self.user)
                self.name = profile.first_name
                self.phone = profile.phone
                self.company = profile.company_name

            # Get Data from AppInfo
            self.snabb_nif = get_app_info('nif')
            self.snabb_name = get_app_info('name')
            self.snabb_company = get_app_info('company')
            self.snabb_phone = get_app_info('phone')
            self.snabb_address = get_app_info('address')
            self.snabb_region = get_app_info('region')
            self.snabb_zipcode = get_app_info('zipcode')
            self.snabb_country = get_app_info('country')
            self.snabb_city = get_app_info('city')
            self.tax = get_app_info('tax')

        super(ReceiptUser, self).save(*args, **kwargs)


class LineReceiptUser(models.Model):
    """Model LineReceipt for User."""

    line_receipt_user_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    receipt_user = models.ForeignKey(
        ReceiptUser, null=False,
        related_name='ReceiptUser', verbose_name="ReceiptUser"
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
            str(self.line_receipt_user_id) + ' - ' +
            str(self.receipt_user.receipt_reference)
        )

    class Meta:
        verbose_name = u'Line Receipt User',
        verbose_name_plural = u'Lines Receipt User'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.line_receipt_user_id:
            self.created_at = int(format(datetime.now(), u'U'))
        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(LineReceiptUser, self).save(*args, **kwargs)


class ReceiptCourier(models.Model):
    """Model Receipt For Courier."""

    receipt_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    courier = models.ForeignKey(
        Courier, related_name='Bill_Courier', verbose_name="Courier",
        blank=True, null=True, on_delete=models.SET_NULL
    )
    receipt_delivery = models.ForeignKey(
        'deliveries.Delivery', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='Receipt_Courier_Delivery', verbose_name="Delivery"
    )
    receipt_reference = models.CharField(
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

    updated_at = models.IntegerField(default=0, editable=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)

    def __str__(self):
        # return str(self.receipt_id + ' - ' + self.receipt_reference)
        return str(self.receipt_id)

    class Meta:
        verbose_name = u'Receipt Courier',
        verbose_name_plural = u'Receipts Courier'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.receipt_id:
            self.created_at = int(format(datetime.now(), u'U'))
            prefix = get_app_info('prefix_receipt_user', 'SNABB')
            serie = get_app_info('serie_receipt_user', 'C')
            year = str(datetime.now().year)
            receipts_count = ReceiptCourier.objects.all().count()
            num = str(receipts_count+1)
            self.receipt_reference = prefix+'-'+year+'-'+serie+'-'+num

            if self.receipt_delivery:
                self.courier = self.receipt_delivery.courier

            if self.courier:
                self.name = self.courier.name
                self.phone = self.courier.phone
                self.fee = self.courier.fee

            # Get Data from AppInfo
            self.snabb_nif = get_app_info('nif')
            self.snabb_name = get_app_info('name')
            self.snabb_company = get_app_info('company')
            self.snabb_phone = get_app_info('phone')
            self.snabb_address = get_app_info('address')
            self.snabb_region = get_app_info('region')
            self.snabb_zipcode = get_app_info('zipcode')
            self.snabb_country = get_app_info('country')
            self.snabb_city = get_app_info('city')
            self.tax = get_app_info('tax')

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(ReceiptCourier, self).save(*args, **kwargs)


class LineReceiptCourier(models.Model):
    """Model LineReceipt for Courier."""

    line_receipt_courier_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    receipt_courier = models.ForeignKey(
        ReceiptCourier, null=False,
        related_name='ReceiptCourier', verbose_name="ReceiptCourier"
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
            str(self.line_receipt_courier_id) + ' - ' +
            str(self.receipt_courier.receipt_reference)
        )

    class Meta:
        verbose_name = u'Line Receipt Courier',
        verbose_name_plural = u'Lines Receipt Courier'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.line_receipt_courier_id:
            self.created_at = int(format(datetime.now(), u'U'))
        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(LineReceiptCourier, self).save(*args, **kwargs)


@receiver(post_save, sender=ReceiptCourier)
def create_lines_receipt_courier(sender, instance, **kwargs):
    """Create lines for Receipt Courier when is created."""
    receipt = instance
    # Execute only when receipt is created
    if receipt.created_at == receipt.updated_at and receipt.total==0:
        delivery = receipt.receipt_delivery
        line = LineReceiptCourier()
        line.receipt_courier = receipt
        line.price = delivery.price
        line.description = 'Delivery #' + str(delivery.delivery_id)
        line.task = 'Task 1'
        line.quantity = 1
        line.discount = 0
        line.total = (line.price * line.quantity) - line.discount
        line.save()
        receipt.updated_at += 1
        receipt.total = line.total
        receipt.save()


@receiver(post_save, sender=ReceiptUser)
def create_lines_receipt_user(sender, instance, **kwargs):
    """Create lines for Receipt User when is created."""
    receipt = instance
    # Execute only when receipt is created
    if receipt.created_at == receipt.updated_at and receipt.total==0:
        delivery = receipt.receipt_delivery
        line = LineReceiptUser()
        line.receipt_user = receipt
        line.price = delivery.price
        line.description = 'Delivery #' + str(delivery.delivery_id)
        line.task = 'Task 1'
        line.quantity = 1
        line.discount = 0
        line.total = (line.price * line.quantity) - line.discount
        line.save()
        receipt.updated_at += 1
        receipt.total = line.total
        receipt.save()
