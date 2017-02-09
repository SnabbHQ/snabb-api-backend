# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Quote
from .serializers import QuoteSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponse
from snabb.address.models import Address
from snabb.address.views import _check_address


class QuoteViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows to create and get a quote
    """

    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()

    def get_queryset(self):
        queryset = Quote.objects.filter(quote_user=self.request.user)
        # queryset = Quote.objects.all()
        return queryset

    def list(self, request):
        print ('vas va listar')
        entries = self.queryset
        serializer = QuoteSerializer(entries, many=True)
        return Response(serializer.data)

    def create(self, request):
        print ('vas va crear')
        received = request.data

        response = {
            'data': {
                'code': 400301,
                'message': 'First Name is required',
                'key': 'FIRST_NAME_REQUIRED'
            },
            'status': status.HTTP_400_BAD_REQUEST
        }

        if not request.user.is_authenticated():  # Check if is authenticated
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        # Data to create a quote
        user = self.request.user

        try:  # Check Quote first_name
            pickup_contact_first_name = received['pickup']['contact']['first_name']
        except Exception as error:
            response['data']['code'] = 400301
            response['data']['message'] = 'Pickup first_name is required',
            response['data']['key'] = 'PICKUP_FIRST_NAME_REQUIRED'
            response['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response)

        try:  # Check Quote last_name
            pickup_contact_last_name = received['pickup']['contact']['last_name']
        except Exception as error:
            response['data']['code'] = 400302
            response['data']['message'] = 'Pickup last_name is required',
            response['data']['key'] = 'PICKUP_LAST_NAME_REQUIRED'
            response['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response)

        try:  # Check Quote company_name
            pickup_contact_company_name = received['pickup']['contact']['company_name']
        except Exception as error:
            response['data']['code'] = 400303
            response['data']['message'] = 'Pickup company_name is required',
            response['data']['key'] = 'PICKUP_COMPANY_NAME_REQUIRED'
            response['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response)

        try:  # Check Quote phone
            pickup_contact_phone = received['pickup']['contact']['phone']
        except Exception as error:
            response['data']['code'] = 400304
            response['data']['message'] = 'Pickup phone is required',
            response['data']['key'] = 'PICKUP_PHONE_REQUIRED'
            response['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response)

        try:  # Check Quote email
            pickup_contact_email = received['pickup']['contact']['email']
        except Exception as error:
            response['data']['code'] = 400305
            response['data']['message'] = 'Pickup email is required',
            response['data']['key'] = 'PICKUP_EMAIL_REQUIRED'
            response['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response)

        try:  # Check Quote address
            pickup_address_address = received['pickup']['address']['address']
        except Exception as error:
            response['data']['code'] = 400306
            response['data']['message'] = 'Pickup address is required',
            response['data']['key'] = 'PICKUP_ADDRESS_REQUIRED'
            response['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response)

        try:  # Check Quote coordinates
            pickup_address_coordinates = received['pickup']['address']['coordinates']
        except Exception as error:
            response['data']['code'] = 400307
            response['data']['message'] = 'Pickup coordinates is required',
            response['data']['key'] = 'PICKUP_COORDINATES_REQUIRED'
            response['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response)

        try:  # Check Quote zipcode
            pickup_address_coordinates = received['pickup']['address']['zipcode']
        except Exception as error:
            response['data']['code'] = 400308
            response['data']['message'] = 'Pickup zipcode is required',
            response['data']['key'] = 'PICKUP_ZIPCODE_REQUIRED'
            response['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response)

        try:  # Check Quote city
            pickup_address_city = received['pickup']['address']['city']
        except Exception as error:
            response['data']['code'] = 400309
            response['data']['message'] = 'Pickup city is required',
            response['data']['key'] = 'PICKUP_CITY_REQUIRED'
            response['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response)

        try:  # Check Quote first_name
            dropoff_contact_first_name = received['dropoff']['contact']['first_name']
        except Exception as error:
            response['data']['code'] = 400311
            response['data']['message'] = 'dropoff first_name is required',
            response['data']['key'] = 'DROPOFF_FIRST_NAME_REQUIRED'
            response['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response)

        try:  # Check Quote last_name
            dropoff_contact_last_name = received['dropoff']['contact']['last_name']
        except Exception as error:
            response['data']['code'] = 400312
            response['data']['message'] = 'dropoff last_name is required',
            response['data']['key'] = 'DROPOFF_LAST_NAME_REQUIRED'
            response['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response)

        try:  # Check Quote company_name
            dropoff_contact_company_name = received['dropoff']['contact']['company_name']
        except Exception as error:
            response['data']['code'] = 400313
            response['data']['message'] = 'dropoff company_name is required',
            response['data']['key'] = 'DROPOFF_COMPANY_NAME_REQUIRED'
            response['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response)

        try:  # Check Quote phone
            dropoff_contact_phone = received['dropoff']['contact']['phone']
        except Exception as error:
            response['data']['code'] = 400314
            response['data']['message'] = 'DROPOFF phone is required',
            response['data']['key'] = 'dropoff_PHONE_REQUIRED'
            response['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response)

        try:  # Check Quote email
            dropoff_contact_email = received['dropoff']['contact']['email']
        except Exception as error:
            response['data']['code'] = 400315
            response['data']['message'] = 'dropoff email is required',
            response['data']['key'] = 'DROPOFF_EMAIL_REQUIRED'
            response['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response)

        try:  # Check Quote address
            dropoff_address_address = received['dropoff']['address']['address']
        except Exception as error:
            response['data']['code'] = 400316
            response['data']['message'] = 'dropoff address is required',
            response['data']['key'] = 'DROPOFF_ADDRESS_REQUIRED'
            response['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response)

        try:  # Check Quote coordinates
            dropoff_address_coordinates = received['dropoff']['address']['coordinates']
        except Exception as error:
            response['data']['code'] = 400317
            response['data']['message'] = 'dropoff coordinates is required',
            response['data']['key'] = 'DROPOFF_COORDINATES_REQUIRED'
            response['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response)

        try:  # Check Quote Zipcode
            dropoff_address_zipcode = received['dropoff']['address']['zipcode']
        except Exception as error:
            response['data']['code'] = 400318
            response['data']['message'] = 'dropoff zipcode is required',
            response['data']['key'] = 'DROPOFF_ZIPCODE_REQUIRED'
            response['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response)

        try:  # Check Quote city
            dropoff_address_city = received['dropoff']['address']['city']
        except Exception as error:
            response['data']['code'] = 400319
            response['data']['message'] = 'Dropoff city is required',
            response['data']['key'] = 'DROPOFF_CITY_REQUIRED'
            response['status'] = status.HTTP_400_BAD_REQUEST
            return Response(response)


        # Validate Address pickup/dropoff
        #     --> Returns zipcode_id
        #         --> create address
        #             --> returns address_id

        # new_pickup_address = Address()
        # new_pickup_address.zipcode = zipcode_id
        # new_pickup_address.address = pickup_address_address
        # coordinates = pickup_address_coordinates
        # new_pickup_address.save()

        # new_dropoff_address = Address()
        # new_dropoff_address.zipcode = zipcode_id
        # new_dropoff_address.address = dropoff_address_address
        # coordinates = dropoff_address_coordinates
        # new_dropoff_address.save()


        # --> create a quote
        # new_quote = Quote()
        # new_quote.quote_user = user
        # new_quote.save()

        # create contact
        #     --> returns contact_id


        

        # address_id - contact_id - quote_id
        #     --> create a Pickup/Dropoff

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        print ('vas va update')
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        print ('destroy')
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
