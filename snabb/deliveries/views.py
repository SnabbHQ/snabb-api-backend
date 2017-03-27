# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Delivery
from snabb.address.models import Address
from snabb.location.models import City
from snabb.contact.models import Contact
from .serializers import DeliverySerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponse
from snabb.utils.code_response import get_response
from datetime import datetime, timedelta
from django.utils.dateformat import format


class DeliveryViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows to create and get a delivery
    """

    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()

    def get_queryset(self):
        queryset = Delivery.objects.filter(
            delivery_quote__quote_user=self.request.user)
        return queryset

    def list(self, request):
        entries = Delivery.objects.filter(
            delivery_quote__quote_user=self.request.user)
        serializer = DeliverySerializer(entries, many=True)
        return Response(serializer.data)
