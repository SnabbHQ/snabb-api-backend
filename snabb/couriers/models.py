# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.dateformat import format
from django.db.models.signals import pre_delete, post_save, m2m_changed
import uuid
from snabb.dispatching.utils import (
    _create_team,
    _update_team,
    _delete_team,
    _get_team_detail,
    _create_worker,
    _get_worker_detail,
    _update_worker,
    _delete_worker
    )


class Team(models.Model):
    team_id = models.AutoField(
        primary_key=True, blank=True, editable=False)
    team_onfleet_id = models.CharField(
        verbose_name="Onfleet ID", max_length=500, null=True, blank=True)
    name = models.CharField(
        verbose_name="Name", max_length=500, null=True, blank=True)

    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name = u'Team'
        verbose_name_plural = u'Teams'

    def team_detail(self):
        "Returns team info from dispatching platform."
        team_details = _get_team_detail(self.team_onfleet_id)
        return team_details

    team_detail = property(team_detail)

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.team_id:
            self.created_at = int(format(datetime.now(), u'U'))
            # We generate an Onfleet Team linked to this Team.
            if not self.team_onfleet_id:
                new_team = _create_team(self.name)
                self.team_onfleet_id = new_team['id']

        else:
            orig = Team.objects.get(pk=self.pk)
            if (self.name != orig.name):
                _update_team(self.name, self.team_onfleet_id)

        super(Team, self).save(*args, **kwargs)


class Courier(models.Model):
    courier_id = models.AutoField(
        primary_key=True, blank=True, editable=False)
    courier_onfleet_id = models.CharField(
        verbose_name="Onfleet ID", max_length=500, null=True, blank=True)
    name = models.CharField(
        verbose_name="Name", max_length=500, null=False, blank=False)
    phone = models.CharField(
        verbose_name=u'Phone', help_text='Example: +34625188877',
        max_length=15, null=False, blank=False
    )
    teams = models.ManyToManyField(
        Team, related_name='teams', null=False, blank=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)
    updated_at = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return u'%s ( %s )' % (self.name, self.phone)

    class Meta:
        verbose_name = u'Courier'
        verbose_name_plural = u'Couriers'

    def courier_details(self):
        "Returns Courier info from dispatching platform."
        courier_details = _get_worker_detail(self.courier_onfleet_id)
        return courier_details

    courier_details = property(courier_details)

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.courier_id:
            self.created_at = int(format(datetime.now(), u'U'))
        else:
            orig = Courier.objects.get(pk=self.pk)
            if (self.name != orig.name):
                _update_worker(
                    worker_id=instance.courier_id, name=self.name, teams=None)

        super(Courier, self).save(*args, **kwargs)


def create_worker(sender, instance, created, **kwargs):
    if created:
        instance.created = True

post_save.connect(
    create_worker, sender=Courier, dispatch_uid="create_worker")


def teams_changed(sender, instance, **kwargs):
    if hasattr(instance, 'created') and not instance.courier_onfleet_id:
        # Create Onfleet courier only when we alve almost 1 team selected.
        if instance.teams.all().count() > 0:
            courier_teams = []
            for team in instance.teams.all():
                courier_teams.append(team.team_onfleet_id)
            new_worker = _create_worker(instance.name, instance.phone, courier_teams)
            instance.courier_onfleet_id = new_worker['id']
            instance.save()
    else:
        if instance.teams.all().count() > 0:
            courier_teams = []
            for team in instance.teams.all():
                courier_teams.append(team.team_onfleet_id)
            _update_worker(worker_id=instance.courier_onfleet_id, name=None, teams=courier_teams)

m2m_changed.connect(teams_changed, sender=Courier.teams.through)


def delete_team(sender, instance, **kwargs):
    try:
        _delete_team(instance.team_onfleet_id)
    except Exception as error:
        print(error)

pre_delete.connect(
    delete_team, sender=Team, dispatch_uid="delete_team")


def delete_courier(sender, instance, **kwargs):
    try:
        _delete_worker(instance.courier_onfleet_id)
    except Exception as error:
        print(error)

pre_delete.connect(
    delete_courier, sender=Courier, dispatch_uid="delete_courier")
