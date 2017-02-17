# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Quote, Place, Task
from snabb.address.models import Address
from snabb.location.models import City
from snabb.contact.models import Contact
from .serializers import QuoteSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponse
from snabb.utils.code_response import get_response
from snabb.geo_utils.utils import (
    _check_api_address, _get_location_info
)


def cancel_quote(task_list, place_list, address_list, contact_list, quote):
    for task in task_list:
        print('\tCANCEL task --> ', task)
        task.delete()
        print('\t\tDeleted')
    for place in place_list:
        print('\tCANCEL place --> ', place)
        place.delete()
        print('\t\tDeleted')
    for address in address_list:
        print('\tCANCEL address --> ', address)
        address.delete()
        print('\t\tDeleted')
    for contact in contact_list:
        print('\tCANCEL contact --> ', contact)
        contact.delete()
        print('\t\tDeleted')

    print('\tCANCEL QUOTE --> ', quote)
    quote.delete()
    print('\t\tDeleted')


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
        entries = Quote.objects.filter(quote_user=self.request.user)
        serializer = QuoteSerializer(entries, many=True)
        return Response(serializer.data)

    def create(self, request):
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

        task_list = []
        place_list = []
        address_list = []
        contact_list = []

        task_order = 0

        for task in received['tasks']:
            # CHECK order, type
            task_order += 1

            try:  # Check Task first_name
                task_contact_first_name = task['contact']['first_name']
            except Exception as error:
                cancel_quote(task_list, place_list, address_list, contact_list, new_quote)
                return Response(get_response(400301))

            try:  # Check Address last_name
                task_contact_last_name = task['contact']['last_name']
            except Exception as error:
                cancel_quote(task_list, place_list, address_list, contact_list, new_quote)
                return Response(get_response(400302))

            try:  # Check Address company_name
                task_contact_company_name = task['contact']['company_name']
            except Exception as error:
                cancel_quote(task_list, place_list, address_list, contact_list, new_quote)
                return Response(get_response(400303))

            try:  # Check Address phone
                task_contact_phone = task['contact']['phone']
            except Exception as error:
                cancel_quote(task_list, place_list, address_list, contact_list, new_quote)
                return Response(get_response(400304))

            try:  # Check Address email
                task_contact_email = task['contact']['email']
            except Exception as error:
                cancel_quote(task_list, place_list, address_list, contact_list, new_quote)
                return Response(get_response(400305))

            try:  # Check Address address
                task_address_address = task['place']['address']
                check_address = _check_api_address(str(task_address_address))

                if check_address['data']['code'] != 200206:
                    cancel_quote(task_list, place_list, address_list, contact_list, new_quote)
                    return Response(
                        get_response(check_address['data']['code'])
                    )
                else:
                    location_info = _get_location_info(task_address_address)
                    api_city = location_info['city']
                    api_zipcode = location_info['zipcode']
                    api_latitude = location_info['latitude']
                    api_longitude = location_info['longitude']

                    if not api_latitude or not api_longitude:
                            cancel_quote(task_list, place_list, address_list, contact_list, new_quote)
                            return Response(get_response(400306))
                    # api_country = location_info['country']
                    # api_region = location_info['region']
                    # api_route = location_info['route']

            except Exception as error:
                print(error)
                cancel_quote(task_list, place_list, address_list, contact_list, new_quote)
                return Response(get_response(400306))

            try:  # Check Place Description
                task_place_description = task['place']['description']
            except Exception as error:
                task_place_description = ''

            try:  # Check comments
                task_comments = task['comments']
            except Exception as error:
                task_comments = None
                # Falta PONER RETURN ERROR

            try:  # Check type
                task_type = task['type']
            except Exception as error:
                if task_type != 'pickup' and task_type != 'dropoff':
                    cancel_quote(task_list, place_list, address_list, contact_list, new_quote)
                    return Response(get_response(400311))

            # Validate Zipcode/city
            if api_zipcode:
                zipcode_task = api_zipcode
            else:
                zipcode_task = None

            try:
                city_task = City.objects.get(
                    google_short_name=api_city,
                    active=True,
                )
            except Exception as error:
                cancel_quote(task_list, place_list, address_list, contact_list, new_quote)
                print(error)
                return Response(get_response(400407))

            # Save Address
            new_task_address = Address()
            new_task_address.zipcode = zipcode_task
            new_task_address.address = task_address_address
            new_task_address.address_city = city_task
            new_task_address.latitude = api_latitude
            new_task_address.longitude = api_longitude
            new_task_address.save()
            address_list.append(new_task_address)
            # print('ADDRESS SAVED')

            # Create  contact
            new_task_contact = Contact()
            new_task_contact.first_name = task_contact_first_name
            new_task_contact.last_name = task_contact_last_name
            new_task_contact.company_name = task_contact_company_name
            new_task_contact.phone = task_contact_phone
            new_task_contact.email = task_contact_email
            new_task_contact.contact_user = user
            new_task_contact.save()
            contact_list.append(new_task_contact)
            # print('CONTACT SAVED')

            # Create place
            new_task_place = Place()
            new_task_place.description = task_place_description
            new_task_place.place_address = new_task_address
            new_task_place.save()
            place_list.append(new_task_place)
            # print('PLACE SAVED')

            # Create Task
            new_task_task = Task()
            new_task_task.task_place = new_task_place
            new_task_task.task_contact = new_task_contact
            new_task_task.order = task_order
            new_task_task.task_type = task_type
            new_task_task.comments = task_comments
            new_task_task.save()
            task_list.append(new_task_task)
            # print('TASK SAVED')

            # Assign task to quote
            new_quote.tasks.add(new_task_task)
            # print('ASIGN TASK TO QUOTE SAVED')

        # Save quote
        new_quote.save()
        # print('QUOTE GUARDADA ', new_quote)

        serializer = QuoteSerializer(new_quote, many=False)
        return Response(serializer.data)
        # return Response(get_response(200205))

    def update(self, request, pk=None):
        # print ('update')
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        # print ('destroy')
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
