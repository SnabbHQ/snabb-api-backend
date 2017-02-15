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


def _check_google_address(address):
    ''' Check if address is valid '''

    if 'address' not in address.keys():  # Check keys
        return get_response(400401)

    # Data to send
    api_key = 'AIzaSyBenCk9al8Bj5Gms0-G11Ug1jaKt0sf2mo'
    address_google = urllib.parse.quote_plus(address['address'])

    webURL = urllib.request.urlopen(
        "https://maps.googleapis.com/maps/api/geocode/json?address=" +
        address_google + "&key=" + api_key + "&language=en"
    )
    webURLdata = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    respJSON = json.loads(webURLdata.decode(encoding))

    try:  # Check if has data
        address_components = respJSON['results'][0]['address_components']
    except Exception as error:
        return get_response(400407)

    google_city = None     # [locality]                    --> short_name
    google_country = None  # [country]                     --> short_name
    google_zipcode = None  # [postal_code]                 --> short_name
    google_region = None   # [administrative_area_level_1] --> short_name
    google_route = None    # [route]                       --> short_name
    google_location = respJSON['results'][0]['geometry']  # --> Coords Google

    for comp in address_components:
        for address_type in comp['types']:
            if address_type == 'locality':
                google_city = comp['short_name']
            if address_type == 'country':
                google_country = comp['short_name']
            if address_type == 'postal_code':
                google_zipcode = comp['short_name']
            if address_type == 'administrative_area_level_1':
                google_region = comp['short_name']
            if address_type == 'route':
                google_route = comp['short_name']

    # print ('city --> ', google_city)
    # print ('country -->', google_country)
    # print ('zipcode -->', google_zipcode)
    # print ('region --> ', google_region)
    # print ('route --> ', google_route)

    if not google_route:  # Check if has route
        return get_response(400402)

    try:  # Check Country
        country = Country.objects.get(iso_code=google_country, active=True)
    except Exception as error:
        return get_response(400403)

    try:  # Check Region
        region = Region.objects.get(
            google_short_name=google_region, active=True
        )
    except Exception as error:
        return get_response(400404)

    if google_zipcode:  # Check Valid Zipcode
        try:
            zipcode = Zipcode.objects.get(
                code=google_zipcode, active=True,
                zipcode_city__google_short_name=google_city,
                zipcode_city__active=True
            )
        except Exception as error:
            return get_response(400405)
    else:  # Check City
        try:
            city = City.objects.get(google_short_name=google_city, active=True)
        except Exception as error:
            return get_response(400406)

    return get_response(200206)
