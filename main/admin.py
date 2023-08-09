from django.contrib import admin
from .models import *

admin.site.register(Storage)
admin.site.register(Nomenclature)
admin.site.register(Flaw)
admin.site.register(Worker)
admin.site.register(ProductionStorage)
admin.site.register(DeliveryNote)
admin.site.register(Specification)
admin.site.register(Crates)
admin.site.register(THD)
admin.site.register(TempCrate)
admin.site.register(RejectionAct)
admin.site.register(settings)