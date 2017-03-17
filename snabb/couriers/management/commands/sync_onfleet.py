# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from snabb.couriers.models import Team, Courier
from snabb.dispatching.utils import (
    _get_all_teams,
    _get_all_workers
    )


class Command(BaseCommand):

    # Displayed from 'manage.py help mycommand'
    help = "Command to sync Onfleet with local BBDD"

    def handle(self, *app_labels, **options):
        """
        Command to sync Onfleet with local BBDD
        """

        onfleet_teams = _get_all_teams()
        onfleet_workers = _get_all_workers()

        local_teams = Team.objects.all().values_list('team_onfleet_id', flat=True)
        local_couriers = Courier.objects.all().values_list('courier_onfleet_id', flat=True)

        for team in onfleet_teams:
            if team['id'] not in local_teams:
                print(team)
                new_team = Team()
                new_team.team_onfleet_id = team['id']
                new_team.name = team['name']
                new_team.save()
            else:
                print('Team already exists')

        for courier in onfleet_workers:
            if courier['id'] not in local_couriers:
                new_courier = Courier()
                new_courier.courier_onfleet_id = courier['id']
                new_courier.name = courier['name']
                new_courier.phone = courier['phone']
                new_courier.save()
                courier_teams = courier['teams']
                new_teams = []
                for team in courier_teams:
                    current_team = Team.objects.get(team_onfleet_id=team)
                    new_teams.append(current_team.pk)
                new_courier.teams.add(*new_teams)

            else:
                print('Courier already exists')

        return 'Local BBDD updated.'
