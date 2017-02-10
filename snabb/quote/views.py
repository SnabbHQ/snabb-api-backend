# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Quote
from snabb.address.models import Address
from snabb.location.models import Zipcode
from snabb.contact.models import Contact
from .serializers import QuoteSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponse
from snabb.utils.code_response import get_response


class QuoteViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows to create and get a quote
    """

    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()

    def get_queryset(self):
        queryset = Quote.objects.filter(quote_user=self.request.user)
        return queryset

    def list(self, request):
        print ('list')
        entries = self.queryset
        serializer = QuoteSerializer(entries, many=True)
        return Response(serializer.data)

    def create(self, request):
        print ('create')
        received = request.data

        if not request.user.is_authenticated():  # Check if is authenticated
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        # Data to create a quote
        user = self.request.user

        try:  # Check Quote first_name
            pickup_contact_first_name = received['pickup']['contact']['first_name']
        except Exception as error:
            return Response(get_response(400301))

        try:  # Check Quote last_name
            pickup_contact_last_name = received['pickup']['contact']['last_name']
        except Exception as error:
            return Response(get_response(400302))

        try:  # Check Quote company_name
            pickup_contact_company_name = received['pickup']['contact']['company_name']
        except Exception as error:
            return Response(get_response(400303))

        try:  # Check Quote phone
            pickup_contact_phone = received['pickup']['contact']['phone']
        except Exception as error:
            return Response(get_response(400304))

        try:  # Check Quote email
            pickup_contact_email = received['pickup']['contact']['email']
        except Exception as error:
            return Response(get_response(400305))

        try:  # Check Quote address
            pickup_address_address = received['pickup']['address']['address']
        except Exception as error:
            return Response(get_response(400306))

        try:  # Check Quote coordinates
            pickup_address_coordinates = received['pickup']['address']['coordinates']
        except Exception as error:
            return Response(get_response(400307))

        try:  # Check Quote zipcode
            pickup_address_zipcode = received['pickup']['address']['zipcode']
        except Exception as error:
            return Response(get_response(400308))

        try:  # Check Quote city
            pickup_address_city = received['pickup']['address']['city']
        except Exception as error:
            return Response(get_response(400309))

        try:  # Check Quote first_name
            dropoff_contact_first_name = received['dropoff']['contact']['first_name']
        except Exception as error:
            return Response(get_response(400311))

        try:  # Check Quote last_name
            dropoff_contact_last_name = received['dropoff']['contact']['last_name']
        except Exception as error:
            return Response(get_response(400312))

        try:  # Check Quote company_name
            dropoff_contact_company_name = received['dropoff']['contact']['company_name']
        except Exception as error:
            return Response(get_response(400313))

        try:  # Check Quote phone
            dropoff_contact_phone = received['dropoff']['contact']['phone']
        except Exception as error:
            return Response(get_response(400314))

        try:  # Check Quote email
            dropoff_contact_email = received['dropoff']['contact']['email']
        except Exception as error:
            return Response(get_response(400315))

        try:  # Check Quote address
            dropoff_address_address = received['dropoff']['address']['address']
        except Exception as error:
            return Response(get_response(400316))

        try:  # Check Quote coordinates
            dropoff_address_coordinates = received['dropoff']['address']['coordinates']
        except Exception as error:
            return Response(get_response(400317))

        try:  # Check Quote Zipcode
            dropoff_address_zipcode = received['dropoff']['address']['zipcode']
        except Exception as error:
            return Response(get_response(400318))

        try:  # Check Quote city
            dropoff_address_city = received['dropoff']['address']['city']
        except Exception as error:
            return Response(get_response(400319))

        # Validate Zipcode/city
        zipcode_pickup = None
        zipcode_dropoff = None
        try:
            zipcode_pickup = Zipcode.objects.get(
                code=pickup_address_zipcode,
                active=True,
                zipcode_city__name=pickup_address_city,
                zipcode_city__active=True
            )
            zipcode_dropoff = Zipcode.objects.get(
                code=dropoff_address_zipcode,
                active=True,
                zipcode_city__name=dropoff_address_city,
                zipcode_city__active=True
            )
        except Exception as error:
            return Response(get_response(400210))

        # Save Address Pickup
        new_pickup_address = Address()
        new_pickup_address.address_zipcode = zipcode_pickup
        new_pickup_address.address = pickup_address_address
        # coordinates = pickup_address_coordinates
        new_pickup_address.save()

        # Save Address Dropoff
        new_dropoff_address = Address()
        new_dropoff_address.address_zipcode = zipcode_dropoff
        new_dropoff_address.address = dropoff_address_address
        # coordinates = dropoff_address_coordinates
        new_dropoff_address.save()

        # --> create a quote
        new_quote = Quote()
        new_quote.quote_user = user
        new_quote.save()

        # Create pickup contact
        new_pickup_contact = Contact()
        new_pickup_contact.first_name = pickup_contact_first_name
        new_pickup_contact.last_name = pickup_contact_last_name
        new_pickup_contact.company_name = pickup_contact_company_name
        new_pickup_contact.phone = pickup_contact_phone
        new_pickup_contact.email = pickup_contact_email
        new_pickup_contact.save()

        # Create dropff contact
        new_dropoff_contact = Contact()
        new_dropoff_contact.first_name = dropoff_contact_first_name
        new_dropoff_contact.last_name = dropoff_contact_last_name
        new_dropoff_contact.company_name = dropoff_contact_company_name
        new_dropoff_contact.phone = dropoff_contact_phone
        new_dropoff_contact.email = dropoff_contact_email
        new_dropoff_contact.save()

        # Create pickup
        # new_pickup = Pickup()
        # new_pickup.pickup_quote = new_quote
        # new_pickup.pickup_address = new_pickup_address
        # new_pickup.pickup_contact = new_pickup_contact
        # new_pickup.save()

        # Create dropoff
        # new_dropoff = DropOff()
        # new_dropoff.dropoff_quote = new_quote
        # new_dropoff.dropoff_address = new_dropoff_address
        # new_dropoff.dropoff_contact = new_dropoff_contact
        # new_dropoff.save()

        return Response(get_response(200205))

    def update(self, request, pk=None):
        # print ('update')
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        # print ('destroy')
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
