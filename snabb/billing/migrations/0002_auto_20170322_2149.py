# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 21:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('deliveries', '0001_initial'),
        ('billing', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('couriers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderuser',
            name='order_delivery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Order_User_Delivery', to='deliveries.Delivery', verbose_name='Delivery'),
        ),
        migrations.AddField(
            model_name='orderuser',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Bill_User', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='ordercourier',
            name='courier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Bill_Courier', to='couriers.Courier', verbose_name='Courier'),
        ),
        migrations.AddField(
            model_name='ordercourier',
            name='order_delivery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Order_Courier_Delivery', to='deliveries.Delivery', verbose_name='Delivery'),
        ),
        migrations.AddField(
            model_name='lineorderuser',
            name='order_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OrderUser', to='billing.OrderUser', verbose_name='OrderUser'),
        ),
        migrations.AddField(
            model_name='lineordercourier',
            name='order_courier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OrderCourier', to='billing.OrderCourier', verbose_name='OrderCourier'),
        ),
    ]
