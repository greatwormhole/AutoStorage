from django.contrib import admin
from django.urls import path
from .views import DeliveryView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('barcode', DeliveryView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)