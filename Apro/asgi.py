from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import os
from time import time

import main.routing
from main.caching import set_cache, get_cache, static_cache_keys
from storage.storage_visual import full_cell_info, blocked_cell_info

def setup():

    start = time()
    print('123')
    cached_info = get_cache(static_cache_keys['full_info_cells'], None)
    cached_blocked = get_cache(static_cache_keys['blocked_cells'], None)

    if cached_info is None:
        print('123')
        data = full_cell_info()
        print('123')
        set_cache(static_cache_keys['full_info_cells'], data, as_list=False)

    if cached_blocked is None:
        print('123')
        data = blocked_cell_info()
        print('123')
        set_cache(static_cache_keys['blocked_cells'], data, as_list=False)

    print(f'Setup in {time() - start} s')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Apro.settings')

django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
'http': django_asgi_app,
'websocket': AuthMiddlewareStack(
        URLRouter(
            main.routing.websocket_urlpatterns
        )
    )

})

setup()