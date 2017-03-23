# -*- coding: utf-8 -*-

'''
    - Library to integrate all onfleet related services
'''

from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
import json


class Onfleet(object):
    api_root = settings.ONFLEET_API_ROOT
    api_key = settings.ONFLEET_API_KEY

    def _get_workers_by_location(self, lat, lon, *args, **kwargs):
        ''' Get Data from API '''
        try:
            # Data to send
            url = self.api_root + "workers/location?longitude=" \
                + lon + "&latitude=" + lat + "&radius=6000"
            apiCall = requests.get(url, auth=HTTPBasicAuth(self.api_key, ''))
            if apiCall.status_code == 200:
                response = apiCall.json()
                return response
            else:
                return None

        except Exception as error:
            print (error)
        return None

    def _create_task(self, destination, recipients, notes, pickupTask=False,
                     completeAfter=None, completeBefore=None, container=None,
                     *args, **kwargs):
        ''' Create task '''

        '''
        curl -X POST "https://onfleet.com/api/v2/tasks" \
       -u "cd3b3de84cc1ee040bf06512d233719c:" \
       -d '{"destination":{"address":{"unparsed":"2829 Vallejo St, SF, CA, USA"},
       "notes":"Small green door by garage door has pin pad, enter *4821*"},
       "recipients":[{"name":"Blas Silkovich","phone":"650-555-4481","notes":"Knows Neiman,
       VIP status."}],"completeAfter":1455151071727,
       "notes":"Order 332: 24oz Stumptown Finca res Leches","autoAssign":{"mode":"distance"}}'
        '''
        '''
        destination / string or object
        The ID of the task's destination or a valid Destination object.

        recipients / string array or object array
        An array containing zero or one IDs of the task's recipients or a valid
        array of zero or one Recipient objects.

        completeAfter / number
        Optional. A timestamp for the earliest time the task should be
        completed.

        completeBefore / number
        Optional. A timestamp for the latest time the task should be completed.

        pickupTask / boolean
        Optional. Whether the task is a pickup task.

        dependencies / string array
        Optional. One or more IDs of tasks which must be completed prior to
        this task.

        notes / string
        Optional. Notes for the task.

        autoAssign / object
        Optional. The automatic assignment options for the newly created task.
        You may not provide a container if using automatic assignment.

        container / object
        Optional. The container to which to append this task. Defaults to the
        creator organization container.

        quantity / number
        Optional. The number of units to be dropped off while completing this
        task, for route optimization purposes.

        serviceTime / number
        Optional. The number of minutes to be spent by the worker on arrival
        at this task's destination, for route optimization purposes.
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
