# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import datetime
from django.http import Http404, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from snabb.billing.models import(
    OrderUser, LineOrderUser,
    OrderCourier, LineOrderCourier
)
from rest_framework.views import APIView
from weasyprint import HTML


class OrderCourierPDF(APIView):

    def get(self, request):
        """Returns Order PDF from Courier."""

        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        if not request.GET.get('order_id'):
            raise Http404("Order does not exist")

        pk = request.GET.get('order_id')
        order = get_object_or_404(OrderCourier, pk=pk)
        lines = get_object_or_404(LineOrderCourier, order_courier=pk)

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
            'lines': lines,
            'dateOrder': dateOrder,
            'total': total
        }

        html_string = render_to_string('orderCourier.html', data)
        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/tmpPDF.pdf');
        fs = FileSystemStorage('/tmp')
        with fs.open('tmpPDF.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="'+order.order_reference+'.pdf"'
            return response

        return response



class OrderUserPDF(APIView):

    def get(self, request):
        """Returns Order PDF from User."""

        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        if not request.GET.get('order_id'):
            raise Http404("Order does not exist")

        pk = request.GET.get('order_id')
        order = get_object_or_404(OrderUser, pk=pk)
        lines = get_object_or_404(LineOrderUser, order_user=pk)
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
            'lines': lines,
            'dateOrder': dateOrder,
            'total': total
        }
        html_string = render_to_string('orderUser.html', data)
        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/tmpPDF.pdf');
        fs = FileSystemStorage('/tmp')
        with fs.open('tmpPDF.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="'+order.order_reference+'.pdf"'
            return response

        return response
