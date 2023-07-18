from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import main, NomenclatureView
urlpatterns = [
    path('storage/consignment-note', main.as_view(), name='consignment-note'),
    path('API/get-all-nomenclature', NomenclatureView.as_view(), name='get_all_nomenclature'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)