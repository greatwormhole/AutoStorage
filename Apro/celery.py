from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Apro.settings')

app = Celery('Apro')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'shift_result': {
        'task': 'plan.tasks.shift_result',
        'schedule': crontab(minute='*/5', hour='8-10'),
    },
    'day_plan': {
        'task': 'plan.tasks.day_plan',
        'schedule': crontab(minute='*/5', hour = '11-12'),
    },
    'month_plan': {
        'task': 'plan.tasks.month_plan',
        'schedule': crontab(day_of_month='1', minute=0, hour='8-10'),
    },
    'rejections_acts_checking': {
        'task': 'main.tasks.check_rejection_acts',
        'schedule': crontab(hour='*/1'),
    },

}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))