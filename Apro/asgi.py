import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import main.routing
from main.caching import set_cache, get_cache, static_cache_keys
from main.storage_visual import full_cell_info

def setup():
    
    cached = get_cache(static_cache_keys['full_info_cells'], None)

    if cached is None:
        data = full_cell_info()
        set_cache(static_cache_keys['full_info_cells'], data, as_list=False)

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