# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Payment, Card as CardDjango
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from decimal import *
from snabb.utils.code_response import get_response
from .serializers import CardSerializer
from snabb.deliveries.models import Delivery
from pinax.stripe.models import Card, Customer
from pinax.stripe.actions import charges, customers, sources
from snabb.stripe_utils.utils import *


class CardViewSet(viewsets.ModelViewSet):

    """
        API endpoint that allows to create, list, and delete Cards
    """

    serializer_class = CardSerializer
    queryset = CardDjango.objects.all()
    http_method_names = ['get', 'post', 'delete', 'patch']

    def partial_update(self, request, pk=None):
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        received = request.data

        if(received['default_card'] == True):
            if not pk:
                response = get_response(400605)
                return Response(data=response['data'], status=response['status'])
            card = CardDjango.objects.get(pk=pk)
            customer = customers.get_customer_for_user(user=request.user)
            if not customer:
                response = get_response(400603)
                return Response(data=response['data'], status=response['status'])

            response = set_default_source(customer, card.card_info['id'])
            return Response(data=response['data'], status=response['status'])
        else:
            response = get_response(400608)
            return Response(data=response['data'], status=response['status'])

    def list(self, request):
        '''
            List all stripe cards of User.
        '''
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        if request.user.is_superuser:
            entries = self.queryset
        else:
            entries = CardDjango.objects.filter(user_id=self.request.user)
        serializer = CardSerializer(entries, many=True)
        return Response(serializer.data)

    def create(self, request):
        '''
            Create a stripe card.
        '''
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        received = request.data

        if 'token' not in received:
            response = get_response(400600)
            return Response(data=response['data'], status=response['status'])

        token = received['token']
        user = User.objects.get(pk=self.request.user.pk)

        try:  # Get/create Customer
            customer = get_or_create_customer(user)
        except Exception as error:
            response = get_response(400603)
            return Response(data=response['data'], status=response['status'])

        try:  # Create Card
            card_selected = create_card(customer, token)
        except Exception as error:
            response = get_response(400604)
            return Response(data=response['data'], status=response['status'])

        try:  # Create Django Card
            new_card = CardDjango.objects.get(
                fingerprint=card_selected.fingerprint
            )
        except CardDjango.DoesNotExist:
            # Check if the first card of this user.
            new_card = CardDjango()
            if CardDjango.objects.filter(user_id=user).count() == 0:
                new_card.default_card = True
            new_card.user_id = user
            new_card.fingerprint = card_selected.fingerprint
            new_card.save()

        sync_stripe_data(customer)  # Sync Data with Stripe

        response = get_response(200208)
        return Response(data=response['data'], status=response['status'])
