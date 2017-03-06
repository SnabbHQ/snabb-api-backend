# -*- coding: utf-8 -*-

'''
    - Library to integrate all onfleet related services
'''

from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
import json


class Onfleet(object):

    api_key = settings.ONFLEET_API_KEY

    def _get_workers_by_location(self, lat, lon, *args, **kwargs):
        ''' Get Data from API '''
        try:
            # Data to send
            url = "https://onfleet.com/api/v2/workers/location?longitude=" \
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

    def _get_task_detail(self, task_info, *args, **kwargs):
        ''' Get Data from a task '''
        '''
        curl -X GET "https://onfleet.com/api/v2/tasks/qNMz6CKwQ*26FOslywsiQxhY" \
               -u "cd3b3de84cc1ee040bf06512d233719c:"
        '''
        return None

    def _create_team(self, team_name, *args, **kwargs):
        ''' Create a team in onfleet '''
        try:
            # Data to send
            payload = {'name': team_name}
            url = "https://onfleet.com/api/v2/teams"
            apiCall = requests.post(
                url, data=json.dumps(payload), auth=HTTPBasicAuth(self.api_key, '')
            )
            print(apiCall.status_code)
            if apiCall.status_code == 201:
                response = apiCall.json()
                return response
            else:
                return None
        except Exception as error:
            print (error)
        return None

    def _update_team(self, team_name, *args, **kwargs):
        ''' Update a team in onfleet '''

        '''
        $ curl -X PUT "https://onfleet.com/api/v2/teams/FFqPs1KHayxorfA~~xIj0us4" \
               -u "cd3b3de84cc1ee040bf06512d233719c:" \
               -d '{"name":"team test","workers":["3joS0Jh19VpJZgSTxFOK9fTf"]}'
        '''

        return None

    def _get_team_detail(self, team_id, *args, **kwargs):
        ''' Get detail of a team from onfleet '''
        '''
        $ curl -X GET "https://onfleet.com/api/v2/teams/9dyuPqHt6kDK5JKHFhE0xihh" \
               -u "cd3b3de84cc1ee040bf06512d233719c:"
        '''
        return None

    def _delete_team(self, team_id, *args, **kwargs):
        ''' Get detail of a team from onfleet '''
        '''
        curl -X DELETE "https://onfleet.com/api/v2/teams/FFqPs1KHayxorfA~~xIj0us4" \
               -u "cd3b3de84cc1ee040bf06512d233719c:"
        '''
        return None

    def _create_worker(self, worker_info, *args, **kwargs):
        ''' Create a worker in onfleet '''
        '''
        curl -X POST "https://onfleet.com/api/v2/workers" \
       -u "cd3b3de84cc1ee040bf06512d233719c:" \
       -d '{"name":"A Swartz","phone":"617-342-8853",
       "teams":["nz1nG1Hpx9EHjQCJsT2VAs~o"],"vehicle":{"type":"CAR",
       "description":"Tesla Model 3","licensePlate":"FKNS9A","color":"purple"}}'
        '''
        return None

    def _get_worker_detail(self, worker_id, *args, **kwargs):
        ''' Get Data from a courier '''
        '''
        curl -X GET "https://onfleet.com/api/v2/workers/rz0LxUnP7uZClvoOuEw75Rii"
        -u "e283ea5e6153b34d9128944656dce3b3:"
        '''
        return None

    def _update_worker(self, worker_info, *args, **kwargs):
        ''' Get Data from a courier '''
        '''
        curl -X PUT "https://onfleet.com/api/v2/workers/sFtvhYK2l26zS0imptJJdC2q" \
               -u "cd3b3de84cc1ee040bf06512d233719c:" \
               -d '{"name":"Laura P","teams":["lHCUJFvh6v0YDURKjokZbvau"]}'
        '''
        return None
