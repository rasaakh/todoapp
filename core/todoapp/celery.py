import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todoapp.settings")

import django
django.setup()

from celery import Celery


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todoapp.settings")

app = Celery("todoapp")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

from todolist.tasks import remove_completed_tasks

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(600.0, remove_completed_tasks.s(), name='Remove Tasks every 10 minutes')
