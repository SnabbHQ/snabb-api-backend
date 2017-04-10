# -*- coding: utf-8 -*-

from background_task import background
from django.utils.dateformat import format
from .models import Delivery
from snabb.quote.models import Task
import time


@background(queue='deliveries')
def assign_delivery(delivery_id):
    '''
    For this tastk we need:
    - Try to get an available courier.
    - Try to assign all tasks to same courier.
    Available delivery statuses:
        ('new', 'new'),
        ('processing', 'processing'),
        ('assigned', 'assigned'),
        ('in_progress', 'in_progress'),
        ('completed', 'completed'),
        ('expired', 'expired'),
        ('cancelled', 'cancelled'),
    '''

    now = time.strftime("%c")
    print ('[TASK] Assign Delivery [/TASK]')
    print ("\t[DATE] --> " + time.strftime("%c") + " <--[DATE]")

    try:  # Get Delivery
        delivery = Delivery.objects.get(delivery_id=delivery_id)
    except Exception as error:
        print (error)
        return False

    # Check if delivery is already cancelled
    if delivery.status == 'cancelled':
        # Return False, with this, we remove this task from the queue.
        # SI es cancelled, completo esta y creo otra en 30 seg.
        return False
    elif delivery.status == 'new':
        delivery.status = 'processing'
        delivery.save()

    print ('\t\t[ID] --> ' + str(delivery.delivery_id) +
           ' ' + str(delivery.status) + ' <--[ID]')

    # Comprobamos created_at + 30 min.
    #   - SI han pasado MAS de 30 machine
    #        - STATUS = EXPIRED, completo task.
    #   - SI NO HAN pasado 30 min.
    #       -intento obtener courier
    #           - Si existe courier, completo task.
    #           - SI NO hay courier, completo esta y creo otra en 30 seg ?
