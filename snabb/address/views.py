# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .utils import _check_google_address


class ValidateAddress(APIView):
    ''' API endpoint that allows validate an address. '''

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        response = _check_google_address(request.data)
        return Response(response)
