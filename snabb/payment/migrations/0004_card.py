# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 14:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0003_auto_20170405_1316'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('card_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fingerprint', models.CharField(max_length=250, verbose_name='FingerPrint')),
                ('created_at', models.IntegerField(blank=True, default=0, editable=False)),
                ('updated_at', models.IntegerField(default=0, editable=False)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Cards',
                'verbose_name': 'Card',
            },
        ),
    ]
