# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.dateformat import format
from django.db.models.signals import pre_delete
import uuid


class Courier(models.Model):
    courier_apiuser = models.OneToOneField(
        User, related_name='Courier_User', null=True, blank=True,
        editable=True, on_delete=models.SET_NULL)
    courier_id = models.AutoField(
        primary_key=True, blank=True, editable=False)
    courier_onfleet_id = models.CharField(
        verbose_name="Onfleet ID", max_length=500, null=True, blank=True)
    name = models.CharField(
        verbose_name="Name", max_length=500, null=True, blank=True)
    phone = models.CharField(
        verbose_name=u'Phone', max_length=15, null=True, blank=True
    )
    password = models.CharField(
        max_length=800, null=True, blank=True
    )
    active = models.BooleanField(default=True, blank=True)

    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return u'%s ( %s )' % (self.name, self.phone)

    class Meta:
        verbose_name = u'Courier'
        verbose_name_plural = u'Couriers'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.courier_id:
            self.created_at = int(format(datetime.now(), u'U'))
            # We generate a Django User linked to this profile.
            user = User.objects.create_user(
                self.phone,
                self.phone,
                self.password)
            user.save()
            self.password = ''
            self.courier_apiuser = user

        else:
            orig = Courier.objects.get(pk=self.pk)

            if ((self.password != "" or
                 self.phone != orig.phone)):

                user = User.objects.get(username=orig.phone)
                if self.password != "":
                    user.set_password(self.password)
                    self.password = ""
                if self.phone != orig.phone:
                    user.username = self.phone
                    user.email = self.phone
                user.save()

        super(Courier, self).save(*args, **kwargs)


def delete_user(sender, instance, **kwargs):
    try:
        instance.courier_apiuser.delete()
    except:
        pass


pre_delete.connect(
    delete_user, sender=Courier, dispatch_uid="delete_user")
