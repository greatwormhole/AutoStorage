from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import main, NomenclatureView, SaveConsignmentNote, defectiveProductCreate, SaveCrateView
urlpatterns = [
    path('storage/consignment-note', main.as_view(), name='consignment-note'),
    path('API/get-all-nomenclature', NomenclatureView.as_view(), name='get_all_nomenclature'),
    path('API/save-consignment-note', SaveConsignmentNote.as_view(), name='save_consignment_note'),
    path('storage/defective-product-add', defectiveProductCreate.as_view(), name='defective_product_add'),
    path('API/save-crate', SaveCrateView.as_view(), name='save_crate'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)