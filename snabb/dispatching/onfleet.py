# -*- coding: utf-8 -*-

'''
    - Library to integrate all onfleet related services
'''

from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
import json
from snabb.utils.utils import get_app_info


class Onfleet(object):
    api_root = settings.ONFLEET_API_ROOT
    api_key = settings.ONFLEET_API_KEY

    def _get_workers_by_location(self, lat, lon, *args, **kwargs):
        ''' Get Data from API '''
        radius = get_app_info('dispatching_radius', '6000')
        try:
            # Data to send
            url = self.api_root + "workers/location?longitude=" \
                + lon + "&latitude=" + lat + "&radius=" + radius
            apiCall = requests.get(url, auth=HTTPBasicAuth(self.api_key, ''))
            if apiCall.status_code == 200:
                response = apiCall.json()
                return response
            else:
                return None

        except Exception as error:
            print (error)
        return None

    def _create_task(self, destination, recipients, notes, dependencies,
                     pickupTask=False, completeAfter=None, completeBefore=None,
                     container=None, *args, **kwargs):
        ''' Create task '''

        '''
        http://docs.onfleet.com/docs/tasks
        '''

        try:
            payload = {}
            if destination is not None:
                # Address from task_place
                payload['destination'] = destination

            if recipients is not None:
                payload['recipients'] = recipients

            if completeAfter is not None:
                payload['completeAfter'] = completeAfter

            if completeBefore is not None:
                payload['completeBefore'] = completeBefore

            payload['pickupTask'] = pickupTask

            if notes is not None:
                payload['notes'] = notes

            if container is not None:
                payload['container'] = container

            payload['dependencies'] = dependencies
            url = self.api_root + "tasks"
            apiCall = requests.post(
                url, data=json.dumps(payload),
                auth=HTTPBasicAuth(self.api_key, '')
            )

            if apiCall.status_code == 200:
                response = apiCall.json()
                return response
            else:
                return None
        except Exception as error:
            print (error)
        return None

    def _assign_task(self, task_id, worker_id, *args, **kwargs):
        ''' Assign task to a worker '''
        try:
            # We need to make a container and update it on the task_id
            container = {}
            container['type'] = 'WORKER'
            container['worker'] = worker_id

            # Data to send
            payload = {'container': container}
            url = self.api_root + "tasks/" + str(task_id)
            apiCall = requests.put(
                url, data=json.dumps(payload),
                auth=HTTPBasicAuth(self.api_key, '')
            )
            if apiCall.status_code == 200:
                response = apiCall.json()
                return response
            else:
                return None
        except Exception as error:
            print (error)
        return None

    def _get_task_detail(self, task_id, *args, **kwargs):
        ''' Get Data from a task '''
        try:
            url = self.api_root + "tasks/" + task_id
            apiCall = requests.get(url, auth=HTTPBasicAuth(self.api_key, ''))
            if apiCall.status_code == 200:
                response = apiCall.json()
                return response
            else:
                return None

        except Exception as error:
            print (error)
        return None

    def _delete_task(self, task_id, *args, **kwargs):
        ''' Delete a task from onfleet '''
        try:
            # Data to send
            url = self.api_root + "tasks/" + str(task_id)
            apiCall = requests.delete(
                url, auth=HTTPBasicAuth(self.api_key, ''))
            if apiCall.status_code == 200:
                return apiCall.status_code
            else:
                return None
        except Exception as error:
            print (error)
        return None

    def _create_team(self, team_name, *args, **kwargs):
        ''' Create a team in onfleet '''
        try:
            # Data to send
            payload = {'name': team_name}
            url = self.api_root + "/teams"
            apiCall = requests.post(
                url, data=json.dumps(payload),
                auth=HTTPBasicAuth(self.api_key, '')
            )
            if apiCall.status_code == 200:
                response = apiCall.json()
            else:
                return None
        except Exception as error:
            print (error)
        return None

    def _update_team(self, team_name, team_id, *args, **kwargs):
        ''' Update team in onfleet '''
        try:
            # Data to send
            payload = {'name': team_name}
            url = self.api_root + "teams/" + str(team_id)
            apiCall = requests.put(
                url, data=json.dumps(payload),
                auth=HTTPBasicAuth(self.api_key, '')
            )
            if apiCall.status_code == 200:
                response = apiCall.json()
                return response
            else:
                return None
        except Exception as error:
            print (error)
        return None

    def _get_team_detail(self, team_id, *args, **kwargs):
        ''' Get detail of a team from onfleet '''
        try:
            url = self.api_root + "teams/" + str(team_id)
            apiCall = requests.get(url, auth=HTTPBasicAuth(self.api_key, ''))
            if apiCall.status_code == 200:
                response = apiCall.json()
                return response
            else:
                return None

        except Exception as error:
            print (error)
        return None

    def _delete_team(self, team_id, *args, **kwargs):
        ''' Delete a team from onfleet '''
        try:
            # Data to send
            url = self.api_root + "teams/" + str(team_id)
            apiCall = requests.delete(
                url, auth=HTTPBasicAuth(self.api_key, ''))
            if apiCall.status_code == 200:
                return apiCall.status_code
            else:
                return None
        except Exception as error:
            print (error)
        return None

    def _get_all_teams(self, *args, **kwargs):
        ''' Get all Teams from API '''
        try:
            # Data to send
            url = self.api_root + "teams"
            apiCall = requests.get(url, auth=HTTPBasicAuth(self.api_key, ''))
            if apiCall.status_code == 200:
                response = apiCall.json()
                return response
            else:
                return None

        except Exception as error:
            print (error)
        return None

    def _create_worker(self, name, phone, teams, *args, **kwargs):
        ''' Create a worker in onfleet '''
        '''
        For now, we don't create a new vehicle for each
        courier, we only send basic info.
        '''
        try:
            # Data to send
            payload = {'name': name, 'phone': phone, 'teams': teams}
            url = self.api_root + "workers"
            apiCall = requests.post(
                url, data=json.dumps(payload),
                auth=HTTPBasicAuth(self.api_key, '')
            )
            if apiCall.status_code == 200:
                response = apiCall.json()
                return response
            else:
                return None
        except Exception as error:
            print (error)
        return None

    def _get_worker_detail(self, worker_id, *args, **kwargs):
        ''' Get Data from a courier '''
        try:
            url = "https://onfleet.com/api/v2/workers/" + str(worker_id)
            apiCall = requests.get(url, auth=HTTPBasicAuth(self.api_key, ''))
            if apiCall.status_code == 200:
                response = apiCall.json()
                return response
            else:
                return None

        except Exception as error:
            print (error)
        return None

    def _update_worker(self, worker_id,
                       name=None, teams=None, *args, **kwargs):
        ''' Get Data from a courier '''
        try:
            # Data to send
            payload = {}
            if name is not None:
                payload['name'] = name

            if teams is not None:
                payload['teams'] = teams

            # payload = {'name': name, 'teams': teams}
            url = self.api_root + "workers/" + str(worker_id)
            apiCall = requests.put(
                url, data=json.dumps(payload),
                auth=HTTPBasicAuth(self.api_key, '')
            )
            if apiCall.status_code == 200:
                response = apiCall.json()
                return response
            else:
                return None
        except Exception as error:
            print (error)
        return None

    def _delete_worker(self, worker_id, *args, **kwargs):
        ''' Delete a worker from onfleet '''
        try:
            # Data to send
            url = self.api_root + "workers/" + str(worker_id)
            apiCall = requests.delete(
                url, auth=HTTPBasicAuth(self.api_key, ''))
            if apiCall.status_code == 200:
                return apiCall.status_code
            else:
                return None
        except Exception as error:
            print (error)
        return None

    def _get_all_workers(self, *args, **kwargs):
        ''' Get all Workers from API '''
        try:
            # Data to send
            url = self.api_root + "workers"
            apiCall = requests.get(url, auth=HTTPBasicAuth(self.api_key, ''))
            if apiCall.status_code == 200:
                response = apiCall.json()
                return response
            else:
                return None

        except Exception as error:
            print (error)
        return None
