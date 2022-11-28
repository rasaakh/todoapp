from celery import shared_task
from .models import Task


@shared_task
def remove_completed_tasks():
    Task.objects.filter(complete = True).delete()


# @shared_task
# def remove_tasks():
#     Task.objects.all().delete()


# @shared_task
# def test():
#    print("send test")