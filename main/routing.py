from django.urls import re_path

from .consumers import THDWS, StorageVisualizingWS

websocket_urlpatterns = [
    re_path(r'ws/THD-ws/(?P<room>\w+)$', THDWS.as_asgi()),
    re_path(r'ws/storage-ws/(?P<id>\d+)$', StorageVisualizingWS.as_asgi())
]