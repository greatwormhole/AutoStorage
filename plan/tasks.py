from Apro.celery import app

@app.task
def test():
   print('This is task message')