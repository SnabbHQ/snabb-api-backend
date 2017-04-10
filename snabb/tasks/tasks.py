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
    _get_available_workers_by_location,
    _send_dispatching
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
    print ('[TASK] Assign Delivery [/TASK]')
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

    creation_time = delivery.created_at
    limit_time = datetime.datetime.now() - datetime.timedelta(minutes=30)
    limit_time = int(format(limit_time, u'U'))

    if creation_time < limit_time:
        delivery.status = 'expired'
        delivery.save()
        return True
    else:
        # Get all tasks for this delivery.
        delivery_tasks = delivery.delivery_quote.tasks.all().order_by('order')
        # Get first task GEO info.
        origin_task = delivery_tasks[:1][0]
        lat = str(origin_task.task_place.place_address.latitude)
        lon = str(origin_task.task_place.place_address.longitude)
        size = delivery.size
        # We need to get a courier for this delivery.
        available_courier = _get_available_workers_by_location(lat, lon, size)

        if available_courier is not None:
            # We have an available courier.

            # TO DO
            # Pending add at this point a dependencies task. TO keep the order
            # of completion

            task_id = None
            for task in delivery_tasks:
                # Check if task is not currently in Onfleet
                if not task.task_onfleet_id:
                    if task_id is not None:
                        # Assign previous task as dependency
                        created_task = _send_dispatching(task, task_id)
                    else:
                        created_task = _send_dispatching(task)

                    if created_task is not None:
                        task.task_onfleet_id = created_task['id']
                        task.save()

                # We get task id to assign to our selected courier.
                assigned_task = _assign_task(
                    task.task_onfleet_id,
                    available_courier
                )

                task_id = task.task_onfleet_id

            return True
        else:
            print('Any courier available')

            # TO DO
            # Pending to add at this point. We need to create a new task to
            # retry the assignment.

            return True
