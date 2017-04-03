# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Payment
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponse
from snabb.utils.code_response import get_response
from .serializers import PaymentSerializer
from decimal import *



# STRIPE
from pinax.stripe.actions import (
    charges, customers, sources, subscriptions, invoices
)

from pinax.stripe.management.commands import sync_customers, init_customers


from pinax.stripe.models import Card, Plan, Subscription, Invoice, Customer

class PaymentViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows to create and get a quote
    """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


    def create(self, request):
        received = request.data

        if not request.user.is_authenticated():  # Check if is authenticated
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        # Data to create a quote
        user = self.request.user
        user = User.objects.get(pk=4)
        token = 'tok_1A4YOELCS1tnVc47R857fQHE'

        customer = customers.get_customer_for_user(user=user)
        if customer is None:
            customer = customers.create(user=user)


        print('-----------TARJETAS--------')
        # print (customer.default_source)
        print (len(customer.stripe_customer.sources.data))
        print (customer.stripe_customer.sources.data)


        new_card = sources.create_card(customer=customer, token=token)
        print ('------- NEW CARD ----')
        print(new_card)
        print (new_card.fingerprint)
        return Response('vale')


        for card in customer.stripe_customer.sources:
            print ('---CARD---')
            print (card.fingerprint)
            if new_card.fingerprint == card.fingerprint:
                sources.delete_card(customer, new_card.id)
                print ('TARJETA DUPLICADA Y BORRADA')
                new_card = card
                break
            #print (card.exp_month)
            #print (card.exp_year)
            #print (card.last4)
            print (card)


        print ('COMPROBAR TARJETAS DE NUEVO ')
        print (len(customer.stripe_customer.sources.data))
        print (customer.stripe_customer.sources.data)


        if customers.can_charge:
            # Generate charge
            charge = charges.create(
                amount=Decimal(40),
                customer=customer,
                currency="eur",
                description="Test 1",
                source=new_card
            )

        # SyncData
        customers.sync_customer(customer)
        charges.sync_charges_for_customer(customer)

        print('SINCRONIZED---------------')

        return Response("okei")
