import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tivit.settings")

app = Celery("tivit")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "fetch_user_data_every_minute": {
        "task": "api.tasks.fetch_user_data",
        "schedule": crontab(minute="*"),
    },
    "fetch_admin_data_every_minute": {
        "task": "api.tasks.fetch_admin_data",
        "schedule": crontab(minute="*"),
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
