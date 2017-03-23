# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-23 08:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('contact_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=500, null=True, verbose_name='Name')),
                ('last_name', models.CharField(blank=True, max_length=500, null=True, verbose_name='Last name')),
                ('company_name', models.CharField(blank=True, max_length=500, null=True, verbose_name='Company Name')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Phone')),
                ('email', models.CharField(blank=True, max_length=300, null=True, verbose_name='Email')),
                ('active', models.BooleanField(default=True)),
                ('updated_at', models.IntegerField(default=0, editable=False)),
                ('created_at', models.IntegerField(blank=True, default=0, editable=False)),
                ('contact_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Contact_User', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
            ],
            options={
                'verbose_name': ('Contact',),
                'verbose_name_plural': 'Contacts',
            },
        ),
    ]
