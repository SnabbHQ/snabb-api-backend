# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Address
from snabb.location.models import Zipcode
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponse


def _check_address(address):
    ''' Check if address is valid '''
    response = {
        'data': {
            'code': 400204,
            'message': 'Invalid address',
            'key': 'INVALID_ADDRESS'
        },
        'status': status.HTTP_400_BAD_REQUEST
    }
    # Check keys
    if 'zipcode' not in address.keys():
        response['data']['code'] = 400205
        response['data']['message'] = 'Key zipcode is required'
        response['data']['key'] = 'KEY_ZIPCODE_REQUIRED'
        response['status'] = status.HTTP_400_BAD_REQUEST
        return response
    if 'city' not in address.keys():
        response['data']['code'] = 400206
        response['data']['message'] = 'Key city is required'
        response['data']['key'] = 'KEY_CITY_REQUIRED'
        response['status'] = status.HTTP_400_BAD_REQUEST
        return response

    # Check Address
    zipcode = None
    try:
        zipcode = Zipcode.objects.get(
            code=address['zipcode'],
            zipcode_city__name=address['city']
        )
    except:
        response['data']['code'] = 400207
        response['data']['message'] = 'Invalid address'
        response['data']['key'] = 'INVALID_ADDRESS'
        response['status'] = status.HTTP_400_BAD_REQUEST
        return response

    if not zipcode.active:
        response['data']['code'] = 400208
        response['data']['message'] = 'Not active zipcde'
        response['data']['key'] = 'INACTIVE_ZIPCODE'
        response['status'] = status.HTTP_400_BAD_REQUEST
        return response
    if not zipcode.zipcode_city.active:
        response['data']['code'] = 400209
        response['data']['message'] = 'Not active city'
        response['data']['key'] = 'INACTIVE_CITY'
        response['status'] = status.HTTP_400_BAD_REQUEST
        return response

    response['data']['code'] = 200204
    response['data']['message'] = 'Address valid'
    response['data']['key'] = 'ADDRESS_OK'
    response['status'] = status.HTTP_200_OK
    return response


class ValidateAddress(APIView):
    ''' API endpoint that allows validate an address. '''

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        received = request.data
        response = _check_address(received)
        return Response(response)
