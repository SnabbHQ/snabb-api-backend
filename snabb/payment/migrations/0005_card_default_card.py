# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='default_card',
            field=models.BooleanField(default=False, verbose_name='DefaultCard'),
        ),
    ]
