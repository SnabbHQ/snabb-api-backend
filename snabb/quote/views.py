# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Quote, Place, Task
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

        try:  # Check Task first_name
            print (len(received['tasks']))
        except Exception as error:
            return Response(get_response(400300))

        # --> create a quote
        new_quote = Quote()
        new_quote.quote_user = user
        new_quote.save()

        for task in received['tasks']:
            # CHECK order, type

            try:  # Check Task first_name
                task_contact_first_name = task['contact']['first_name']
            except Exception as error:
                new_quote.delete()
                return Response(get_response(400301))

            try:  # Check Address last_name
                task_contact_last_name = task['contact']['last_name']
            except Exception as error:
                new_quote.delete()
                return Response(get_response(400302))

            try:  # Check Address company_name
                task_contact_company_name = task['contact']['company_name']
            except Exception as error:
                new_quote.delete()
                return Response(get_response(400303))

            try:  # Check Address phone
                task_contact_phone = task['contact']['phone']
            except Exception as error:
                new_quote.delete()
                return Response(get_response(400304))

            try:  # Check Address email
                task_contact_email = task['contact']['email']
            except Exception as error:
                new_quote.delete()
                return Response(get_response(400305))

            try:  # Check Address address
                task_address_address = task['place']['address']['address']
            except Exception as error:
                new_quote.delete()
                return Response(get_response(400306))

            try:  # Check Address coordinates
                task_address_coordinates = task['place']['address']['coordinates']
            except Exception as error:
                new_quote.delete()
                return Response(get_response(400307))

            try:  # Check Address zipcode
                task_address_zipcode = task['place']['address']['zipcode']
            except Exception as error:
                new_quote.delete()
                return Response(get_response(400308))

            try:  # Check Address city
                task_address_city = task['place']['address']['city']
            except Exception as error:
                new_quote.delete()
                return Response(get_response(400309))

            try:  # Check Place Description
                task_place_description = task['place']['description']
            except Exception as error:
                new_quote.delete()
                task_place_description = ''

            try:  # Check Order
                task_order = task['order']
            except Exception as error:
                task_order = 0
                # new_quote.delete()
                # Falta PONER RETURN ERROR

            try:  # Check type
                task_type = task['type']
            except Exception as error:
                if task_type != 'pickup' or task_type != 'dropoff':
                    task_type = 'pickup'
                    # new_quote.delete()
                    # Falta PONER RETURN ERROR

            # Validate Zipcode/city
            zipcode_task = None
            try:
                zipcode_task = Zipcode.objects.get(
                    code=task_address_zipcode,
                    zipcode_city__name=task_address_city,
                    active=True,
                    zipcode_city__active=True
                )
            except Exception as error:
                new_quote.delete()
                return Response(get_response(400210))

            # Save Address
            new_task_address = Address()
            new_task_address.address_zipcode = zipcode_task
            new_task_address.address = task_address_address
            # coordinates = task_address_coordinates
            new_task_address.save()

            # Create  contact
            new_task_contact = Contact()
            new_task_contact.first_name = task_contact_first_name
            new_task_contact.last_name = task_contact_last_name
            new_task_contact.company_name = task_contact_company_name
            new_task_contact.phone = task_contact_phone
            new_task_contact.email = task_contact_email
            new_task_contact.save()

            # Create place
            new_task_place = Place()
            new_task_place.description = task_place_description
            new_task_place.place_address = new_task_address
            new_task_place.save()

            # Create Task
            new_task_task = Task()
            new_task_task.task_place = new_task_place
            new_task_task.task_contact = new_task_contact
            new_task_task.order = 0
            new_task_task.task_type = 0
            new_task_task.save()

            # Assign task to quote
            new_quote.tasks.add(new_task_task)

        # Save quote
        new_quote.save()

        return Response(get_response(200205))

    def update(self, request, pk=None):
        # print ('update')
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        # print ('destroy')
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
