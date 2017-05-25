# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-04 13:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0005_auto_20170502_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='tracking_url',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Tracking URL'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_status',
            field=models.CharField(blank=True, choices=[('new', 'new'), ('assigned', 'assigned'), ('in_progress', 'in_progress'), ('completed', 'completed'), ('failed', 'failed')], max_length=300, null=True, verbose_name='Task Status'),
        ),
    ]