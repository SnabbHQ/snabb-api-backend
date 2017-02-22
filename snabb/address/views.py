# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from snabb.geo_utils.utils import _check_api_address
from snabb.utils.code_response import get_response


class ValidateAddress(APIView):
    ''' API endpoint that allows validate an address. '''

    permission_classes = (AllowAny,)

    def post(self, request, format=None):

        if 'address' not in request.data.keys():
            response = get_response(400401)
            return Response(data=response['data'], status=response['status'])

        response = _check_api_address(str(request.data['address']))
        return Response(data=response['data'], status=response['status'])
