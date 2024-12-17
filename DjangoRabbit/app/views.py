from django.http import HttpResponse
from app.tasks import add

def test_celery(request):

    '''function for celery_rabbitmq testing'''

    add.delay(4, 6)

    return HttpResponse("Task is being processed")