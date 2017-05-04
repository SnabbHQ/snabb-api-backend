# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-02 11:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0004_auto_20170402_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_status',
            field=models.CharField(blank=True, choices=[('pickup', 'Pickup'), ('dropoff', 'Dropoff')], max_length=300, null=True, verbose_name='Task Status'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(blank=True, choices=[('pickup', 'Pickup'), ('dropoff', 'Dropoff')], default='new', max_length=300, null=True, verbose_name='Task Type'),
        ),
    ]