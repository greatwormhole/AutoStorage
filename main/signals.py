from Apro.settings import DEBUG
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from .models import Worker, Crates, TempCrate, TEXT_ID_RANK
from .utils import generate_worker_barcode
from .caching import set_crate_cache

if not DEBUG:        
    @receiver(post_save, sender=Worker)
    def create_barcode(instance, created, **kwargs):
        if created:
            generate_worker_barcode(instance.id, instance.name)
        
@receiver(post_save, sender=Crates)
def set_crates_text_id(instance, created, **kwargs):
    if created:
        zero_amount = TEXT_ID_RANK - instance.rank
        instance.text_id = zero_amount * '0' + str(instance.id)
        instance.save()
    
@receiver(post_save, sender=TempCrate)
def set_temp_crates_text_id(instance, created, **kwargs):
    if created:
        zero_amount = TEXT_ID_RANK - instance.rank
        instance.text_id = zero_amount * '0' + str(instance.id)
        instance.save()

@receiver(pre_save, sender=Crates)
def pre_change(sender, instance: Crates, **kwargs):
    original_cell = None
    
    if instance.id:
        original_cell = sender.objects.get(id=instance.id).cell
        
    instance.__original_cell = original_cell

@receiver(pre_save, sender=Crates)
def on_change(instance: Crates, **kwargs):
    if instance.__original_cell != instance.cell:
        data = {
                'crate_id': instance.id,
                'amount': instance.amount,
                'articule': instance.nomenclature.article,
                'cell_adress': instance.cell.adress,
                'storage_name': instance.cell.storage_name,
                'x_coord': instance.cell.x_cell_coord,
                'y_coord': instance.cell.y_cell_coord,
                'z_coord': instance.cell.z_cell_coord,
        }
        set_crate_cache(data)