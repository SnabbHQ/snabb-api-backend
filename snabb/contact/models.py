# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from datetime import datetime
from django.utils.dateformat import format
from django.contrib.auth.models import User


class Contact(models.Model):
    contact_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    first_name = models.CharField(
        verbose_name="Name",
        max_length=500, null=True, blank=True
    )
    last_name = models.CharField(
        verbose_name="Last name",
        max_length=500, null=True, blank=True
    )
    company_name = models.CharField(
        verbose_name="Company Name",
        max_length=500, null=True, blank=True
    )
    phone = models.CharField(
        verbose_name=u'Phone',
        max_length=15, null=True, blank=True
    )
    email = models.CharField(
        verbose_name=u'Email',
        max_length=300, null=True, blank=True
    )
    contact_user = models.ForeignKey(
        User, related_name='Contact_User',
        verbose_name=u'Created by', null=True, blank=True
    )
    active = models.BooleanField(default=True)
    updated_at = models.IntegerField(default=0, editable=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)

    def __str__(self):
        return str(self.contact_id)

    class Meta:
        verbose_name = u'Contact',
        verbose_name_plural = u'Contacts'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.contact_id:
            self.created_at = int(format(datetime.now(), u'U'))

        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(Contact, self).save(*args, **kwargs)
