# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.dateformat import format
import uuid


class Profile(models.Model):
    profile_apiuser = models.OneToOneField(
        User, related_name='Profile_User', null=True, blank=True,
        editable=False, on_delete=models.CASCADE)
    profile_id = models.AutoField(
        primary_key=True, blank=True, editable=False)
    company_name = models.CharField(
        verbose_name="Company Name", max_length=500, null=True, blank=True)
    first_name = models.CharField(
        verbose_name="Name", max_length=500, null=True, blank=True)
    last_name = models.CharField(
        verbose_name="Last name", max_length=500, null=True, blank=True)
    phone = models.CharField(
        verbose_name=u'Phone', max_length=15, null=True, blank=True
    )
    email = models.CharField(
        verbose_name=u'User Email',
        max_length=300, null=False, blank=True
    )
    password = models.CharField(
        max_length=800, null=True, blank=True
    )
    active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    send_email_notifications = models.BooleanField(default=True)
    send_sms_notifications = models.BooleanField(default=True)

    user_lang = models.CharField(
        max_length=3, null=True, blank=True, editable=True)
    profile_activation_key = models.CharField(
        max_length=200, null=True, blank=True, editable=True)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def _get_full_name(self):
        "Returns user full name."
        return '%s %s' % (self.first_name, self.last_surname)

    full_name = property(_get_full_name)

    def __str__(self):
        if self.company_name:
            return u'%s  ( %s )' % (
                self.company_name, self.email)
        else:
            return u'%s %s ( %s )' % (
                self.first_name, self.last_name, self.email)

    class Meta:
        verbose_name = u'Profile'
        verbose_name_plural = u'Profiles'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.profile_id:
            self.created_at = int(format(datetime.now(), u'U'))
            # We generate a Django User linked to this profile.
            user = User.objects.create_user(
                self.email,
                self.email,
                self.password)
            user.save()
            self.password = ''
            self.profile_apiuser = user

        else:
            orig = Profile.objects.get(pk=self.pk)

            if ((self.password != "" or
                 self.email != orig.email)):

                user = User.objects.get(username=orig.email)
                if self.password != "":
                    user.set_password(self.password)
                    self.password = ""
                if self.email != orig.email:
                    user.username = self.email
                    user.email = self.email
                user.save()

        if not self.profile_activation_key:
            self.profile_activation_key = "%s" % (uuid.uuid4(),)

        super(Profile, self).save(*args, **kwargs)
