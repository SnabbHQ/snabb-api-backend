# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import datetime
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render
from snabb.utils.code_response import get_response
from snabb.utils.utils import LargeResultsSetPagination
from rest_framework import viewsets
from snabb.billing.models import(
    ReceiptUser as ReceiptUserModel,
    LineReceiptUser as LineReceiptUserModel,
    ReceiptCourier as ReceiptCourierModel,
    LineReceiptCourier as LineReceiptCourierModel
)
from snabb.billing.serializers import(
    ReceiptUserSerializer,
    ReceiptCourierSerializer
)


class ReceiptUserViewSet(viewsets.ModelViewSet):
    """ViewSet to View Receipt User. """
    queryset = ReceiptUserModel.objects.all()
    serializer_class = ReceiptUserSerializer
    pagination_class = LargeResultsSetPagination


    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        pk = self.kwargs['pk']
        try:
            if request.user.is_superuser:
                receipt = ReceiptUserModel.objects.get(pk=pk)
            else:
                receipt = ReceiptUserModel.objects.get(pk=pk, user=request.user)
        except:
            response = get_response(400501)
            return Response(data=response['data'], status=response['status'])

        lines = LineReceiptUserModel.objects.filter(receipt_user=pk)
        if lines.count()>0:
            line = lines[0]
        else:
            line = '------'
        dateReceipt = (
            datetime.datetime.fromtimestamp(
                int(receipt.created_at)
            ).strftime('%Y-%m-%d %H:%M:%S')
        )

        total = receipt.total
        if receipt.tax > 0:
            total = receipt.total + (receipt.total*receipt.tax/100)

        data = {
            'receipt': receipt,
            'line': line,
            'dateReceipt': dateReceipt,
            'total': total
        }
        return render(self.request, 'receiptUser.html', data)

    def list(self, request):

        if not self.request.user.is_authenticated():
            return HttpResponseForbidden()

        # Filter By Delivery
        if request.GET.get('delivery_id',''):
            entries = ReceiptUserModel.objects.filter(
                receipt_delivery=request.GET.get('delivery_id','')
            )
        else:
            entries = ReceiptUserModel.objects.all()

        serializer = ReceiptUserSerializer(entries, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return HttpResponseForbidden()

        if self.request.user.is_superuser:
            queryset = ReceiptUserModel.objects.all()
        else:
            queryset = ReceiptUserModel.objects.filter(user=self.request.user)

        return queryset


class ReceiptCourierViewSet(viewsets.ModelViewSet):
    """ViewSet to View Receipt Courier. """
    queryset = ReceiptCourierModel.objects.all()
    serializer_class = ReceiptCourierSerializer
    pagination_class = LargeResultsSetPagination

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        if not request.user.is_superuser:
            return HttpResponseForbidden()

        pk = self.kwargs['pk']
        try:
            receipt = ReceiptCourierModel.objects.get(pk=pk)
        except:
            response = get_response(400502)
            return Response(data=response['data'], status=response['status'])

        lines = LineReceiptCourierModel.objects.filter(receipt_courier=pk)
        if lines.count()>0:
            line = lines[0]
        else:
            line = '------'

        dateReceipt = (
            datetime.datetime.fromtimestamp(
                int(receipt.created_at)
            ).strftime('%Y-%m-%d %H:%M:%S')
        )

        base = receipt.total
        total = receipt.total
        fee = 0
        tax = 0
        if receipt.fee > 0:
            fee_percent = receipt.fee
            fee = base * (fee_percent)/100
        if receipt.tax > 0:
            tax_percent = receipt.tax
            tax = (total - fee) * tax_percent/100

        total = total - fee - tax

        data = {
            'receipt': receipt,
            'line': line,
            'base': base,
            'dateReceipt': dateReceipt,
            'fee_percent': fee_percent,
            'fee': fee,
            'tax_percent': tax_percent,
            'tax': tax,
            'total': total
        }
        return render(self.request, 'receiptCourier.html', data)

    def list(self, request):

        if not self.request.user.is_authenticated():
            return HttpResponseForbidden()

        # Filter By Delivery
        if request.GET.get('delivery_id',''):
            entries = ReceiptCourierModel.objects.filter(
                receipt_delivery=request.GET.get('delivery_id','')
            )
        else:
            entries = ReceiptCourierModel.objects.all()

        serializer = ReceiptCourierSerializer(entries, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return HttpResponseForbidden()

        if not self.request.user.is_superuser:
            return HttpResponseForbidden()

        queryset = ReceiptCourierModel.objects.all()
        return queryset
