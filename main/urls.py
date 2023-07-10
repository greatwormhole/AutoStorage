from django.contrib import admin
from django.urls import path
from .views import DeliveryView, HomeView, LoginView, THDList, NomenclatureView, MainView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('barcode', DeliveryView.as_view(), name='barcode'),
    path('API/login', LoginView.as_view(), name='login'),
    path('API/THD_list', THDList.as_view(), name='THD_list'),
    path('API/get_nomenclature', NomenclatureView.as_view(), name='nomenclature'),
    path('API/check_binding', MainView.as_view(), name='binding'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)