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
            name='Profile',
            fields=[
                ('profile_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('company_name', models.CharField(blank=True, max_length=500, null=True, verbose_name='Company Name')),
                ('first_name', models.CharField(blank=True, max_length=500, null=True, verbose_name='Name')),
                ('last_name', models.CharField(blank=True, max_length=500, null=True, verbose_name='Last name')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Phone')),
                ('email', models.CharField(blank=True, max_length=300, verbose_name='User Email')),
                ('password', models.CharField(blank=True, max_length=800, null=True)),
                ('active', models.BooleanField(default=True)),
                ('verified', models.BooleanField(default=False)),
                ('send_email_notifications', models.BooleanField(default=True)),
                ('send_sms_notifications', models.BooleanField(default=True)),
                ('user_lang', models.CharField(blank=True, max_length=3, null=True)),
                ('profile_activation_key', models.CharField(blank=True, max_length=200, null=True)),
                ('reset_password_key', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.IntegerField(blank=True, default=0, editable=False)),
                ('updated_at', models.IntegerField(default=0, editable=False)),
                ('profile_apiuser', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Profile_User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]
