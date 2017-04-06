# -*- coding: utf-8 -*-

from background_task import background
from django.utils.dateformat import format
from snabb.deliveries.models import Delivery
from snabb.quote.models import Task
import time
import datetime
from snabb.dispatching.utils import (
    _create_task,
    _get_task_detail,
    _assign_task,
)


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
        # If delivery is already cancelled, complete the task.
        return True
    elif delivery.status == 'new':
        delivery.status = 'processing'
        delivery.save()

    print ('\t\t[ID] --> ' + str(delivery.delivery_id) +
           ' ' + str(delivery.status) + ' <--[ID]')

    creation_time = delivery.created_at
    limit_time = datetime.datetime.now() - datetime.timedelta(minutes=30)
    limit_time = int(format(limit_time, u'U'))

    if creation_time < limit_time:
        delivery.status = 'expired'
        delivery.save()
        return True
    else:
        print('SEARCH FOR A VALID COURIER')
        # For now, we assign to fixed courier.

        # Get all tasks for this delivery.
        delivery_tasks = delivery.delivery_quote.tasks.all().order_by('order')

        for task in delivery_tasks:
            # Check if task is not currently in Onfleet
            if not task.task_onfleet_id:
                created_task = task.send_dispatching
                print('CREATING TASK')
                if created_task is not None:
                    task.task_onfleet_id = task.send_dispatching['id']
                    task.save()
                    print('CREATE TASK')

            # We get task id to assign to a FIXED courier.
            print('ASSSIGN TASK ' + str(task_onfleet_id))

            assigned_task = _assign_task(
                task.task_onfleet_id,
                'bqHwe8jkWOUA*EtimgJkS4FQ'
            )

        return True

        #   - SI NO HAN pasado 30 min.
        #       -intento obtener courier
        #           - Si existe courier, completo task.
        #               - Obtengo las tasks de el quote actual, y las mando a Onfleet.

        #           - SI NO hay courier, completo esta y creo otra en 30 seg ?
