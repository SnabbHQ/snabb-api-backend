from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponse
from snabb.quote.models import Task
import json
from snabb.utils.utils import get_delivery_from_task


@csrf_exempt
def webhookTask(request):
    # Onfleet needs a URL verification to create a new webhook.
    if request.method == 'GET':
        print(request.GET)
        if 'check' in request.GET:
            return HttpResponse(request.GET['check'], status=status.HTTP_200_OK)
    elif request.method == 'POST':
        '''
        Available triggeId:
        0 = taskStarted (Status = in_progress)
        3 = taskCompleted (Status = completed)
        4 = taskFailed (Status = failed)
        8 = taskDeleted (Status = deleted)
        9 = taskAssigned (Status = assigned)
        '''

        statuses = {
            0: 'in_progress',
            3: 'completed',
            4: 'failed',
            8: 'deleted',
            9: 'assigned',
        }
        data = json.loads(request.body.decode('utf-8'))
        current_trigger = data['triggerId']
        task_id = data['taskId']
        try:
            task = Task.objects.get(task_onfleet_id=task_id)
            task.task_status = statuses[current_trigger]
            task.save()

            if current_trigger == 0:
                # Add trackUrl to task.
                tracking_url = data['data']['task']['trackingURL']
                task.tracking_url = tracking_url
                task.save()
                # Update Delivery status to in_progress
                delivery = get_delivery_from_task(task)
                if delivery is not None:
                    delivery.status = 'in_progress'
                    delivery.save()
                else:
                    print ('Delivery not exists')
            if current_trigger == 3:

                # Update Delivery status to in_progress
                delivery = get_delivery_from_task(task)
                if delivery is not None:
                    delivery_tasks = delivery.delivery_quote.tasks.all().order_by('order')
                    last_task = delivery_tasks.reverse()[0]
                    if last_task.task_status == 'completed':
                        delivery.status = 'completed'
                        delivery.save()
                else:
                    print ('Delivery not exists')

        except Task.DoesNotExist:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        return HttpResponse(status=status.HTTP_200_OK)

    return HttpResponse(status=status.HTTP_200_OK)
