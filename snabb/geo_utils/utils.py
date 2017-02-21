# -*- coding: utf-8 -*-

'''
    - Validate an Address -
        Function to validate an address using external APIs
        Usage: pass an address and the function returns a status code
        Returns a code 200206 if it is valid.
        Set the environment var MAPS_API_PROVIDER to set teh API provider.
'''
from math import radians, cos, sin, asin, sqrt
from django.conf import settings
from geopy.distance import great_circle  # GET distante without any provider

api_provider = settings.MAPS_API_PROVIDER
if api_provider == 'GOOGLE':
    import snabb.geo_utils.google as api_integration


def _get_data_to_api_address(address):
    ''' Get Data Directly from API '''
    return api_integration._get_data_to_api_address(address)


def _get_location_info(address):
    ''' Returns dictionary with location info from address '''
    return api_integration._get_location_info(address)


def _check_api_address(address):
    ''' Check if address is valid '''
    return api_integration._check_api_address(address)


def _check_distance_between_points(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth
    """
    origin = (lat1, lon1)
    destination = (lat2, lon2)
    distance = int(great_circle(origin, destination).meters)
    return distance
