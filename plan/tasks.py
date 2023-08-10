from Apro.celery import app
from .models import Plans

@app.task
def test():
   
   plan = Plans.objects.create(title='TEST')
   print(plan)
   
   return

@app.task
def day_plan():
   pass

@app.task
def month_plan():
   pass

@app.task
def shift_result():
   pass