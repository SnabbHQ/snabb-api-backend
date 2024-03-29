# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-23 08:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('couriers', '0001_initial'),
        ('quote', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('delivery_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('status', models.CharField(choices=[('new', 'new'), ('processing', 'processing'), ('no_couriers_available', 'no_couriers_available'), ('en_route_to_pickup', 'en_route_to_pickup'), ('en_route_to_dropoff', 'en_route_to_dropoff'), ('at_dropoff', 'at_dropoff'), ('completed', 'completed'), ('unable_to_deliver', 'unable_to_deliver'), ('scheduled', 'scheduled')], default='new', max_length=300, verbose_name='Status')),
                ('created_at', models.IntegerField(blank=True, default=0, editable=False)),
                ('updated_at', models.IntegerField(default=0, editable=False)),
                ('courier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delivery_courier', to='couriers.Courier')),
                ('delivery_quote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delivery_quote', to='quote.Quote')),
            ],
            options={
                'verbose_name': 'Delivery',
                'verbose_name_plural': 'Deliveries',
            },
        ),
    ]
