# -*- coding: utf-8 -*-

'''
    - Library to integrate all onfleet related services
'''

from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth


class Onfleet(object):

    api_key = settings.ONFLEET_API_KEY

    def _get_workers_by_location(self, lat, lon, *args, **kwargs):
        ''' Get Data from API '''
        try:
            # Data to send
            url = "https://onfleet.com/api/v2/workers/location?longitude=" \
             + lon + "&latitude=" + lat + "&radius=6000"
            print(url)
            apiCall = requests.get(url, auth=HTTPBasicAuth(self.api_key, ''))
            if apiCall.status_code == 200:
                response = apiCall.json()
                return response
            else:
                return None

            return respJSON
        except Exception as error:
            print (error)
        return None
