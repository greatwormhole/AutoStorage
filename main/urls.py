from django.contrib import admin
from django.urls import path
from .views import DeliveryView, base, LoginView, THDList

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('barcode', DeliveryView.as_view(), name='barcode'),
    path('API/login', LoginView.as_view(), name='login'),
    path('API/THD_list', THDList.as_view(), name='THD_list'),
    path('', base.as_view(), name="base"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)