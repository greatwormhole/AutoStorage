from Apro.settings import DEBUG
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from storage.views import getColor
from .models import Worker, Crates, TempCrate, TEXT_ID_RANK
from .utils import generate_worker_barcode
from .caching import set_cache, get_cache, static_cache_keys

origin_cell = []
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

    origin_cell.append(original_cell)

@receiver(post_save, sender=Crates)
def on_change(instance: Crates, **kwargs):

    moved_crates_data = {}
    blocked_cells_data = {}
    instance.__original_cell = origin_cell[0]
    origin_cell.pop()
    if instance.__original_cell != instance.cell:

        moved_crates_data = {
                'crate_id': instance.text_id,
                'amount': instance.amount,
                'articule': instance.nomenclature.article,
                'cell_adress': instance.cell.adress,
                'cell_origin_adress':instance.__original_cell.adress if instance.__original_cell != None else '',
                'storage_name': instance.cell.storage_name,
                'storage_name_origin':instance.__original_cell.storage_name if instance.__original_cell != None else '',
                'x_coord_origin_cell': instance.__original_cell.x_cell_coord if instance.__original_cell != None else '',
                'y_coord_origin_cell': instance.__original_cell.y_cell_coord if instance.__original_cell != None else '',
                'z_coord_origin_cell': instance.__original_cell.z_cell_coord if instance.__original_cell != None else '',
                'x_coord': instance.cell.x_cell_coord,
                'y_coord': instance.cell.y_cell_coord,
                'z_coord': instance.cell.z_cell_coord,
                'origin_fullness':instance.__original_cell.full_percent if instance.__original_cell != None else '',
                'fullness':instance.cell.full_percent if instance.cell != None else ''
        }
        storage_name = instance.cell.storage_name
        blocked_neighbour_cells = [cell for cell in instance.cell.neighboring_cells() if cell.is_blocked]
        blocked_cells_data = get_cache(static_cache_keys['blocked_cells'], {})
        try:
            for cell in blocked_neighbour_cells:
                blocked_cells_data[storage_name][f'{cell.x_cell_coord}_{cell.y_cell_coord}_{cell.z_cell_coord}'] = cell.full_percent

            if instance.__original_cell is not None:
                storage_name = instance.__original_cell.storage_name
                blocked_neighbour_cells = [cell for cell in instance.__original_cell.neighboring_cells() if not cell.is_blocked]
                for cell in blocked_neighbour_cells:
                    blocked_cells_data[storage_name].pop(f'{cell.x_cell_coord}_{cell.y_cell_coord}_{cell.z_cell_coord}', None)
        except:
            pass
    set_cache(static_cache_keys['moving_crates'], moved_crates_data)
    set_cache(static_cache_keys['blocked_cells'], blocked_cells_data, as_list=False)