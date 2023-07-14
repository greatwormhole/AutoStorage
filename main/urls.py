from django.contrib import admin
from django.urls import path
from .views import (
    DeliveryView,
    HomeView,
    LoginView,
    THDList,
    NomenclatureView,
    MainView,
    THDSelect,
    WebSocketTHDcheck,
    LogoutView,
    CrateView
    )
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('barcode', DeliveryView.as_view(), name='barcode'),
    path('API/login', LoginView.as_view(), name='login'),
    path('API/THD-list', THDList.as_view(), name='THD_list'),
    path('API/get-nomenclature', NomenclatureView.as_view(), name='nomenclature'),
    path('API/THD-lock', MainView.as_view(), name='locking'),
    path('API/THD-select', THDSelect.as_view(), name="THD_select"),
    path('API/THD-check', WebSocketTHDcheck.as_view(), name='websocket_THD_check'),
    path('API/logout', LogoutView.as_view(), name='logout'),
    path('API/crates', CrateView.as_view(), name='crate')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)