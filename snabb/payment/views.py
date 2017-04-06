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
from .serializers import PaymentSerializer, CardSerializer
from snabb.deliveries.models import Delivery
from pinax.stripe.models import Card, Customer
from pinax.stripe.actions import charges, customers, sources
from snabb.stripe_utils.utils import *



class SetDefaultSourceCardViewSet(viewsets.ModelViewSet):

    """
        API endpoint that allows set default card to customer
    """

    serializer_class = CardSerializer
    queryset = CardDjango.objects.all()
    http_method_names = ['retrieve']

    def retrieve(self, request, pk=None):
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        received = request.data

        if 'source_id' not in received:
            response = get_response(400605)
            return Response(data=response['data'], status=response['status'])

        customer = customers.get_customer_for_user(user=user)
        if not customer:
            response = get_response(400603)
            return Response(data=response['data'], status=response['status'])

        response = set_default_source(customer,received['source_id'])
        return Response(data=response['data'], status=response['status'])


class CardViewSet(viewsets.ModelViewSet):

    """
        API endpoint that allows to create, list, and delete Cards
    """

    serializer_class = CardSerializer
    queryset = CardDjango.objects.all()
    http_method_names = ['get', 'post', 'delete']

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

        try: # Get/create Customer
            customer = get_or_create_customer(user)
        except Exception as error:
            response = get_response(400603)
            return Response(data=response['data'], status=response['status'])

        try: # Create Card
            card_selected = create_card(customer, token)
        except Exception as error:
            response = get_response(400604)
            return Response(data=response['data'], status=response['status'])

        try: # Create Django Card
            new_card = CardDjango.objects.get(
                fingerprint=card_selected.fingerprint
            )
        except CardDjango.DoesNotExist:
            new_card = CardDjango()
            new_card.user_id = user
            new_card.fingerprint = card_selected.fingerprint
            new_card.save()

        sync_stripe_data(customer)  # Sync Data with Stripe

        response = get_response(200208)
        return Response(data=response['data'], status=response['status'])

class PaymentViewSet(viewsets.ModelViewSet):
    '''
        API endpoint that allows get all Payments from a user
    '''

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    http_method_names = ['get']


    def list(self, request):

        if not request.user.is_authenticated():
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        if request.user.is_superuser:
            entries = self.queryset
        else:
            entries = Payment.objects.filter(payment_user=self.request.user)
        serializer = PaymentSerializer(entries, many=True)
        return Response(serializer.data)

    def create(self, request):
        received = request.data

        if not request.user.is_authenticated():
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        user = User.objects.get(pk=self.request.user)

        if 'token' not in received:
            response = get_response(400600)
            return Response(data=response['data'], status=response['status'])
        token = received['token']

        # Get delivery Data
        if 'delivery_id' not in received:
            response = get_response(400601)
            return Response(data=response['data'], status=response['status'])
        try:
            delivery = Delivery.objects.get(pk=received['delivery_id'])
        except Delivery.DoesNotExist:
            response = get_response(400602)
            return Response(data=response['data'], status=response['status'])

        # Get/create Customer
        try:
            customer = get_or_create_customer(user)
        except Exception as error:
            response = get_response(400603)
            return Response(data=response['data'], status=response['status'])

        # Create Card
        try:
            card_selected = create_card(customer, token)
        except Exception as error:
            response = get_response(400604)
            return Response(data=response['data'], status=response['status'])

        # Data to Charge
        amount = delivery.price
        currency = 'eur'
        description = 'Delivery ID: ' + str(delivery.delivery_id)

        # Create Charge
        # create_charge(
        #     customer, card_selected, amount, currency, description
        # )

        sync_stripe_data(customer) # Sync Data

        # Generate Django Payment
        payment = Payment()
        payment.payment_user = user
        payment.payment_delivery = delivery
        payment.amount = amount
        payment.currency = currency
        payment.description = description
        payment.status = 'completed'
        payment.save()

        response = get_response(200207)
        return Response(data=response['data'], status=response['status'])
