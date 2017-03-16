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

    def _create_task(self, task_info, *args, **kwargs):
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
                url, data=json.dumps(payload), auth=HTTPBasicAuth(self.api_key, '')
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
            url = self.api_root + "teams/"+str(team_id)
            apiCall = requests.put(
                url, data=json.dumps(payload), auth=HTTPBasicAuth(self.api_key, '')
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
            apiCall = requests.delete(url, auth=HTTPBasicAuth(self.api_key, ''))
            if apiCall.status_code == 200:
                return apiCall.status_code
            else:
                return None
        except Exception as error:
            print (error)
        return None

    def _create_worker(self, name, phone, teams, *args, **kwargs):
        ''' Create a worker in onfleet '''
        '''
        For now, we don't create a new vehicle for each courier,we only send basic info.
        '''
        try:
            # Data to send
            payload = {'name': name, 'phone': phone, 'teams': teams}
            url = self.api_root + "workers"
            apiCall = requests.post(
                url, data=json.dumps(payload), auth=HTTPBasicAuth(self.api_key, '')
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

    def _update_worker(self, worker_id, name=None, teams=None, *args, **kwargs):
        ''' Get Data from a courier '''
        '''
        curl -X PUT "https://onfleet.com/api/v2/workers/sFtvhYK2l26zS0imptJJdC2q" \
               -u "cd3b3de84cc1ee040bf06512d233719c:" \
               -d '{"name":"Laura P","teams":["lHCUJFvh6v0YDURKjokZbvau"]}'
        '''
        try:
            # Data to send
            payload = {}
            if name is not None:
                payload['name'] = name

            if teams is not None:
                payload['teams'] = teams

            # payload = {'name': name, 'teams': teams}
            url = self.api_root + "workers/"+str(worker_id)
            apiCall = requests.put(
                url, data=json.dumps(payload), auth=HTTPBasicAuth(self.api_key, '')
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
            apiCall = requests.delete(url, auth=HTTPBasicAuth(self.api_key, ''))
            if apiCall.status_code == 200:
                return apiCall.status_code
            else:
                return None
        except Exception as error:
            print (error)
        return None
