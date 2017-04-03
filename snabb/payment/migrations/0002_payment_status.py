# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-03 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('processing', 'processing'), ('completed', 'completed'), ('cancelled', 'cancelled')], default='processing', max_length=300, verbose_name='Status'),
        ),
    ]
