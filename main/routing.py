from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/THD-ws/(?P<room>\w+)$', consumers.THDWS.as_asgi())
]