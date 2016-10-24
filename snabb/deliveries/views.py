# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from snabb.deliveries.models import Delivery
from rest_framework import viewsets

from .serializers import DeliverySerializer


class DeliveriesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to get or add deliveries in the system.

    The **owner** of the code snippet may update or delete instances
    of the code snippet.
    """
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
