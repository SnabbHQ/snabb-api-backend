# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-06 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliveries', '0003_auto_20170402_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='size',
            field=models.CharField(blank=True, choices=[('small', 'small'), ('medium', 'medium'), ('big', 'big')], max_length=300, null=True, verbose_name='Size'),
        ),
    ]
