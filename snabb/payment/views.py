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

from snabb.deliveries.models import Delivery

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
    http_method_names = ['get', 'post', 'head']

    def get_or_create_customer(self, user):
        '''
            Get or create a customer stripe from a user
        '''
        # Create/Get Customer Stripe
        customer = customers.get_customer_for_user(user=user)
        if customer is None:
            customer = customers.create(user=user)
        return customer


    def delete_all_cards(self, customer):
        '''
            Erases all cards from Customer
        '''
        for card in customer.stripe_customer.sources:
            sources.delete_card(customer, card.id)

    def create_card(self, customer, token):
        '''
            Creates a new card and erases duplicate cards.
            Returns the selected card
        '''
        # Create New Card
        new_card = sources.create_card(customer=customer, token=token)
        card_selected = new_card

        # Delete Duplicated Cards
        if len(customer.stripe_customer.sources.data) > 0:
            cont = 0
            for card in customer.stripe_customer.sources:
                if new_card.fingerprint == card.fingerprint:
                    if cont == 0:
                        card_selected = card
                    cont += 1
                    if cont > 1:
                        sources.delete_card(customer, card.id)
        # Return Selected Card
        return card_selected

    def create_charge(self, customer, card, amount, currency, description):
        '''
            Create a charge from customer and card
        '''
        if customers.can_charge:
            charge = charges.create(
                customer=customer,
                source=card,
                amount=Decimal(amount),
                currency=currency,
                description=description,
            )

    def sync_stripe_data(self, customer):
        '''
            Sync Data from Django to Stripe
        '''
        customers.sync_customer(customer)
        charges.sync_charges_for_customer(customer)

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

        # user = self.request.user
        # token = 'tok_1A5ECZLCS1tnVc47lWqocJZt'

        # Get User Data
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
            customer = self.get_or_create_customer(user)
        except Exception as error:
            response = get_response(400603)
            return Response(data=response['data'], status=response['status'])

        # Create Card
        try:
            card_selected = self.create_card(customer, token)
        except Exception as error:
            response = get_response(400604)
            return Response(data=response['data'], status=response['status'])

        # Data to Charge
        amount = delivery.price
        currency = 'eur'
        description = 'Delivery ID: ' + str(delivery.delivery_id)

        # Create Charge
        self.create_charge(
            customer, card_selected, amount, currency, description
        )

        # Sync Data
        self.sync_stripe_data(customer)

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
