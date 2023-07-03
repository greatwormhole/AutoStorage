import os
import sys
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Apro.settings')
django_asgi_app = get_asgi_application()
from channels.routing import ProtocolTypeRouter,URLRouter
from .settings import BASE_DIR
import main.routing
import django
from channels.auth import AuthMiddlewareStack
from django.conf import settings
import django
from channels.routing import get_default_application

application = ProtocolTypeRouter({
'http': django_asgi_app,
'websocket': AuthMiddlewareStack(
        URLRouter(
            main.routing.websocket_urlpatterns
        )
    )

})