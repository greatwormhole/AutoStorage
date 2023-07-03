from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Apro.settings')

app = Celery('Apro')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    #'save_db': {
    #'task':'main.tasks.save_db',
        #'schedule': crontab(minute='*/1')},
    'test': {
    'task':'plan.tasks.test',
           'schedule': crontab(minute='*/1')
    }

}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
