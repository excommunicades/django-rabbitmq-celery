from django.http import HttpResponse
from app.tasks import add

def test_celery(request):
    add.delay(4, 6)
    return HttpResponse("Task is being processed")