# -*- coding: utf-8 -*-

'''
    - Validate a Google Address -
        Function to validate a google address
        Usage: pass an address and the function returns a status code
        Returns a code 200206 if it is valid.
'''
import json
import urllib.request
from snabb.utils.code_response import get_response
from snabb.location.models import Zipcode, Region, City, Country
from django.conf import settings


def _get_data_to_api_address(address):
    ''' Get Data from API '''
    try:
        # Data to send
        api_key = settings.MAPS_API_KEY
        address_google = urllib.parse.quote_plus(address)

        webURL = urllib.request.urlopen(
            "https://maps.googleapis.com/maps/api/geocode/json?address=" +
            address_google + "&key=" + api_key + "&language=en"
        )
        webURLdata = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')
        respJSON = json.loads(webURLdata.decode(encoding))
        return respJSON
    except Exception as error:
        print (error)
    return None


def _get_location_info(address):
    ''' Returns dictionary with location info from address '''
    info = {
        'city': None,
        'zipcode': None,
        'region': None,
        'country': None,
        'route': None,
        'latitude': None,
        'longitude': None
    }
    try:
        respJSON = _get_data_to_api_address(address)
        address_components = respJSON['results'][0]['address_components']
        for comp in address_components:
            for address_type in comp['types']:
                if address_type == 'locality':
                    info['city'] = comp['short_name']
                if address_type == 'country':
                    info['country'] = comp['short_name']
                if address_type == 'postal_code':
                    info['zipcode'] = comp['short_name']
                if address_type == 'administrative_area_level_1':
                    info['region'] = comp['short_name']
                if address_type == 'route':
                    info['route'] = comp['short_name']
                if address_type == 'postal_town':
                    info['city'] = comp['short_name']
        try:
            geometry = respJSON['results'][0]['geometry']
            info['latitude'] = geometry['location']['lat']
            info['longitude'] = geometry['location']['lng']
        except Exception as error:
            print (error)
    except Exception as error:
        print (error)
        return None

    return info


def _check_api_address(address):
    ''' Check if address is valid '''
    if not address or address == '':
        return get_response(400401)

    location_info = _get_location_info(address)
    if not location_info:
        return get_response(400407)

    api_city = location_info['city']
    api_zipcode = location_info['zipcode']
    api_country = location_info['country']
    api_region = location_info['region']
    api_route = location_info['route']

    if not api_route:  # Check if has route
        return get_response(400402)

    try:  # Check Country
        country = Country.objects.get(iso_code=api_country, active=True)
    except Exception as error:
        return get_response(400403)
    '''
        # For now, we don't check region.
        try:  # Check Region
            region = Region.objects.get(
                google_short_name=api_region, active=True
            )
        except Exception as error:
            return get_response(400404)
    '''
    if api_zipcode:  # Check Valid Zipcode
        try:
            zipcode = Zipcode.objects.get(
                code=api_zipcode, active=True,
                zipcode_city__google_short_name=api_city,
                zipcode_city__active=True
            )
        except Exception as error:
            return get_response(400405)
    else:  # Check City
        try:
            city = City.objects.get(google_short_name=api_city, active=True)
        except Exception as error:
            return get_response(400406)

    return get_response(200206)

def _get_real_eta(origin_lat,origin_lon,destination_lat,destination_lon,mode):
    ''' Get Data from API '''
    try:
        # Data to send
        api_key = settings.MAPS_API_KEY
        webURL = urllib.request.urlopen(
            "https://maps.googleapis.com/maps/api/directions/json?origin=" +
            str(origin_lat) + "," + str(origin_lon) + "&destination=" +  str(destination_lat) + "," + str(destination_lon) +
            "&key=" + api_key + "&mode=" + mode
        )
        webURLdata = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')
        respJSON = json.loads(webURLdata.decode(encoding))
        eta = respJSON['routes'][0]['legs'][0]['duration']['text']
        return eta
    except Exception as error:
        print (error)
    return None
