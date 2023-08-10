from celery.signals import worker_ready
from celery import group
from datetime import timedelta as td, datetime as dt

from Apro.celery import app
from storage.storage_visual import full_cell_info, blocked_cell_info
from main.caching import set_cache, static_cache_keys
from main.models import settings, RejectionAct

# @app.task
# @worker_ready.connect
# def blocked_cache_set(**kwargs):
#     print('start of blocked')
#     data = blocked_cell_info()
#     set_cache(static_cache_keys['blocked_cells'], data, as_list=False)
#     print('blocked cache done')

# @app.task
# @worker_ready.connect
# def full_info_cache_set(**kwargs):
#     print('start of full')
#     data = full_cell_info()
#     set_cache(static_cache_keys['full_info_cells'], data, as_list=False)
#     print('full cache done')
    
# async def run_on_start():
#     res = await group(
#         blocked_cache_set()
#     )

@app.task
def check_rejection_acts():
    
    timeout_hours = settings.objects.get(setting_name='defective_parts_timeout')
    rejection_acts = RejectionAct.objects.all()
    
    for el in rejection_acts:
        if dt.now() - el.datetime >= td(hours=timeout_hours):
            print(el)