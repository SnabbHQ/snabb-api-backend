# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from snabb.deliveries.models import Delivery, Quote
from rest_framework import viewsets

from .serializers import DeliverySerializer, QuoteSerializer


class DeliveriesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to get or add deliveries in the system
    """
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuotesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to generate a quote for a delivery.
    """
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
