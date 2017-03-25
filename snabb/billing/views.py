# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import datetime
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render
from snabb.utils.code_response import get_response
from rest_framework import viewsets
from snabb.billing.models import(
    OrderUser as OrderUserModel,
    LineOrderUser as LineOrderUserModel,
    OrderCourier as OrderCourierModel,
    LineOrderCourier as LineOrderCourierModel
)
from snabb.billing.serializers import(
    OrderUserSerializer,
    OrderCourierSerializer
)


class OrderUserViewSet(viewsets.ModelViewSet):
    """ViewSet to View Order User. """
    queryset = OrderUserModel.objects.all()
    serializer_class = OrderUserSerializer

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        pk = self.kwargs['pk']
        try:
            if request.user.is_superuser:
                order = OrderUserModel.objects.get(pk=pk)
            else:
                order = OrderUserModel.objects.get(pk=pk, user=request.user)
        except:
            response = get_response(400501)
            return Response(data=response['data'], status=response['status'])

        lines = LineOrderUserModel.objects.filter(order_user=pk)
        if lines.count()>0:
            line = lines[0]
        else:
            line = '------'
        dateOrder = (
            datetime.datetime.fromtimestamp(
                int(order.created_at)
            ).strftime('%Y-%m-%d %H:%M:%S')
        )

        total = order.total
        if order.tax > 0:
            total = order.total + (order.total*order.tax/100)

        data = {
            'order': order,
            'line': line,
            'dateOrder': dateOrder,
            'total': total
        }
        return render(self.request, 'orderUser.html', data)


    def list(self, request):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        if request.user.is_superuser:
            entries = OrderUserModel.objects.all()
        else:
            entries = OrderUserModel.objects.filter(user=self.request.user)

        serializer = OrderUserSerializer(entries, many=True)
        return Response(serializer.data)


class OrderCourierViewSet(viewsets.ModelViewSet):
    """ViewSet to View Order Courier. """
    queryset = OrderCourierModel.objects.all()
    serializer_class = OrderUserSerializer

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        if not request.user.is_superuser:
            return HttpResponseForbidden()

        pk = self.kwargs['pk']
        try:
            order = OrderCourierModel.objects.get(pk=pk)
        except:
            response = get_response(400502)
            return Response(data=response['data'], status=response['status'])

        lines = LineOrderCourierModel.objects.filter(order_courier=pk)
        if lines.count()>0:
            line = lines[0]
        else:
            line = '------'

        dateOrder = (
            datetime.datetime.fromtimestamp(
                int(order.created_at)
            ).strftime('%Y-%m-%d %H:%M:%S')
        )

        total = order.total
        if order.tax > 0:
            total = order.total + (order.total*order.tax/100)

        data = {
            'order': order,
            'line': line,
            'dateOrder': dateOrder,
            'total': total
        }
        return render(self.request, 'orderCourier.html', data)


    def list(self, request):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        if not request.user.is_superuser:
            return HttpResponseForbidden()

        entries = OrderCourierModel.objects.all()
        serializer = OrderCourierSerializer(entries, many=True)
        return Response(serializer.data)
