from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('storage/consignment-note', main.as_view(), name='consignment-note'),
    path('API/get-all-nomenclature', NomenclatureView.as_view(), name='get_all_nomenclature'),
    path('API/save-consignment-note', SaveConsignmentNote.as_view(), name='save_consignment_note'),
    path('storage/defective-product-add', defectiveProductCreate.as_view(), name='defective_product_add'),
    path('API/save-crate', SaveCrateView.as_view(), name='save_crate'),
    path('API/get-nomenclature-crates', NomenclatureCratesView.as_view(), name='get_nomenclature_crates'),
    path('API/crate-positioning', CratePositioningView.as_view(), name='crate_positioning'),
    path('API/choose-crate', SaveTempCrateView.as_view(), name='choose_crate'),
    path('production-storage', storagePlanView.as_view(),name="production_storage"),
    path('storage-navigation', storageNavigation.as_view(),name="storage_navigation"),
    path('storage-visualization', storageVisualization.as_view(),name="storage_visualization"),
    path('API/storage-info', storageInfo.as_view(), name='cells')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)