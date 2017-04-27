# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Delivery
from snabb.address.models import Address
from snabb.location.models import City
from snabb.contact.models import Contact
from snabb.quote.models import Quote
from .serializers import DeliverySerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponse
from snabb.utils.code_response import get_response
from datetime import datetime
from django.utils.dateformat import format
from snabb.utils.utils import LargeResultsSetPagination
from snabb.billing.models import ReceiptUser
from django.db.models import Prefetch
from django.http import HttpResponseForbidden, HttpResponseBadRequest


class DeliveryViewSet(viewsets.ModelViewSet):

    """
    API endpoint that allows to create and get a delivery
    """

    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()
    pagination_class = LargeResultsSetPagination

    def get_serializer_context(self):
        """
        We send the action(retrieve, list,etc..) to our serializer, to check
        if we need to make a call to Onfleet.
        """
        return {
            'action': self.action
        }

    def get_queryset(self):
        query = self.request.query_params

        queryset = Delivery.objects.filter(
            delivery_quote__quote_user=self.request.user).select_related(
                'delivery_quote',
                'courier'
        ).prefetch_related('Receipt_User_Delivery')
        if 'status' in query.keys():
            queryset = queryset.filter(status=query['status'])
        return queryset.order_by('-created_at')

    def create(self, request):
        received = request.data

        if not request.user.is_authenticated():  # Check if is authenticated
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        if 'quote_id' not in received:
            response = get_response(400503)
            return Response(data=response['data'], status=response['status'])
        else:
            try:
                quote = Quote.objects.get(quote_id=received['quote_id'])
            except Quote.DoesNotExist:
                response = get_response(400506)
                return Response(
                    data=response['data'], status=response['status'])

        try:
            delivery = Delivery.objects.get(
                delivery_quote=received['quote_id'])
            response = get_response(400607)
            return Response(
                data=response['data'], status=response['status'])
        except Delivery.DoesNotExist:
            pass

        if 'selected_package_size' not in received:
            response = get_response(400504)
            return Response(data=response['data'], status=response['status'])
        else:
            package_size = received['selected_package_size']

        now = int(format(datetime.now(), u'U'))

        if quote.expire_at < now:
            response = get_response(400507)
            return Response(data=response['data'], status=response['status'])

        new_delivery = Delivery()
        new_delivery.delivery_quote = quote
        new_delivery.status = 'new'
        new_delivery.size = package_size
        new_delivery.price = quote.prices[package_size]['price']
        new_delivery.save()

        serializer = DeliverySerializer(new_delivery, many=False)
        return Response(serializer.data)


class CancelDeliveryViewSet(viewsets.ModelViewSet):

    """
        API endpoint that allows cancel a Delivery
    """

    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    http_method_names = ['get']


    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        try:
            delivery = Delivery.objects.get(
                pk=self.kwargs['pk'], delivery_quote__quote_user=request.user)
            statusAllowedCancelled = [
                'new', 'processing', 'assigned', 'in_progress'
            ]
            if delivery.status in statusAllowedCancelled:
                delivery.status = 'cancelled'
                delivery.save()
                response = get_response(200210)
                return Response(data=response['data'], status=response['status'])
            else:
                response = get_response(400610)
                return Response(data=response['data'], status=response['status'])
        except Exception as error:
            print(error)
            response = get_response(400609)
            return Response(data=response['data'], status=response['status'])

    def list(self, request):
        return HttpResponseBadRequest()

    def create(self, request):
        return HttpResponseBadRequest()

    def get_queryset(self):
        return HttpResponseBadRequest()
