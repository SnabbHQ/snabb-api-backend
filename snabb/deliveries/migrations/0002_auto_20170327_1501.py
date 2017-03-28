# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliveries', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='status',
            field=models.CharField(choices=[('new', 'new'), ('processing', 'processing'), ('assigned', 'assigned'), ('in_progress', 'in_progress'), ('completed', 'completed'), ('expired', 'expired'), ('cancelled', 'cancelled')], default='new', max_length=300, verbose_name='Status'),
        ),
    ]
