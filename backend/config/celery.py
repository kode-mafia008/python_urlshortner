import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('urlshortener')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    'aggregate-analytics-hourly': {
        'task': 'analytics.tasks.aggregate_analytics',
        'schedule': crontab(minute=0),  # Every hour
    },
    'cleanup-old-analytics': {
        'task': 'analytics.tasks.cleanup_old_analytics',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    'update-url-rankings': {
        'task': 'analytics.tasks.update_url_rankings',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
