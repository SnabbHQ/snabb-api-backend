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
            'message': 'Address not valid',
            'key': 'ADDRESS_NOT_VALID'
        },
        'status': status.HTTP_400_BAD_REQUEST
    }

    if 'zipcode' in address.keys():
        try:
            zipcode = Zipcode.objects.get(code=address['zipcode'])
        except:
            return response
        response['data']['code'] = 200204
        response['data']['message'] = 'Address valid'
        response['data']['key'] = 'ADDRESS_OK'
        response['status'] = status.HTTP_200_OK
    else:
        response['data']['code'] = 400205
        response['data']['message'] = 'Key zipcode is required'
        response['data']['key'] = 'KEY_ZIPCODE_REQUIRED'
        response['status'] = status.HTTP_400_BAD_REQUEST

    return response


class ValidateAddress(APIView):
    ''' API endpoint that allows validate an address. '''

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        received = request.data
        response = _check_address(received)
        return Response(response)
