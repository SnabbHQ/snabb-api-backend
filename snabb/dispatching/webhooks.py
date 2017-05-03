from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponse
from snabb.quote.models import Task
import json


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

        except Task.DoesNotExist:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        return HttpResponse(status=status.HTTP_200_OK)

    return HttpResponse(status=status.HTTP_200_OK)
