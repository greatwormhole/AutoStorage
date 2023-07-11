from django.contrib import admin
from django.urls import path
from .views import DeliveryView, HomeView, LoginView, THDList, NomenclatureView, MainView, THDSelect, get_ws, WebSocketTHDcheck

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('test', get_ws),
    path('', HomeView.as_view(), name="home"),
    path('barcode', DeliveryView.as_view(), name='barcode'),
    path('API/login', LoginView.as_view(), name='login'),
    path('API/THD-list', THDList.as_view(), name='THD_list'),
    path('API/get-nomenclature', NomenclatureView.as_view(), name='nomenclature'),
    path('API/check-binding', MainView.as_view(), name='binding'),
    path('API/THD-select', THDSelect.as_view(), name="THD_select"),
    path('API/THD-check', WebSocketTHDcheck.as_view(), name='websocket_THD_check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)