# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-10 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='enterprise',
            field=models.BooleanField(default=False),
        ),
    ]
