from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete

from Apro.settings import DEBUG
from .models import Worker, Crates, TempCrate, TEXT_ID_RANK, Storage
from .utils import generate_worker_barcode
from .caching import set_cache, get_cache, static_cache_keys
from storage.storage_visual import full_cell_info

if not DEBUG:        
    @receiver(post_save, sender=Worker)
    def create_barcode(instance, created, **kwargs):
        if created:
            generate_worker_barcode(instance.id, instance.name)
    
@receiver(post_save, sender=TempCrate)
def on_save(sender, instance, created, **kwargs):
    if created:
        zero_amount = TEXT_ID_RANK - instance.rank
        txt_id = zero_amount * '0' + str(instance.id)
        sender.objects.filter(id=instance.id).update(text_id=txt_id)

@receiver(post_save, sender=Crates)
def on_save(sender, instance, created, **kwargs):
    if created:
        zero_amount = TEXT_ID_RANK - instance.rank
        txt_id = zero_amount * '0' + str(instance.id)
        sender.objects.filter(id=instance.id).update(text_id=txt_id)

@receiver(pre_save, sender=Crates)
def pre_change(sender, instance: Crates, **kwargs):
    original_cell = None

    if instance.id:
        original_cell = sender.objects.get(id=instance.id).cell

    instance.__original_cell = original_cell

@receiver(post_save, sender=Crates)
def on_change(instance: Crates, **kwargs):

    moved_crates_data = {}
    blocked_cells_data = {}
    full_cell_info_data = {}
    
    if instance.__original_cell != instance.cell:
        moved_crates_data = {
                'crate_id': instance.text_id,
                'amount': instance.amount,
                'articule': instance.nomenclature.article,
                'status': 'moved',
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
                'origin_fullness': instance.__original_cell.full_percent if instance.__original_cell != None else '',
                'fullness': instance.cell.full_percent if instance.cell != None else '',
                'is_blocked': instance.cell.is_blocked,
                'is_blocked_origin': instance.__original_cell.is_blocked if instance.__original_cell != None else '',
        }

        storage_name = instance.cell.storage_name
        blocked_neighbour_cells = [cell for cell in instance.cell.neighboring_cells() if cell.is_blocked]

        blocked_cells_data = get_cache(static_cache_keys['blocked_cells'], {})
        full_cell_info_data = get_cache(static_cache_keys['full_info_cells'], {})
        
        if blocked_cells_data.get(storage_name, None) is None and len(blocked_neighbour_cells) > 0:
            blocked_cells_data[storage_name] = {}
        
        for cell in blocked_neighbour_cells:
            blocked_cells_data[storage_name][f'{cell.x_cell_coord}_{cell.y_cell_coord}_{cell.z_cell_coord}'] = cell.full_percent

        full_cell_info_data[instance.cell.storage_name][instance.cell.y_cell_coord][instance.cell.x_cell_coord][instance.cell.z_cell_coord] = [
            instance.cell.visualization_y,
            instance.cell.visualization_x,
            instance.cell.visualization_z,
            instance.cell.full_percent,
        ]

        if instance.__original_cell is not None:
            storage_name = instance.__original_cell.storage_name
            blocked_neighbour_cells = [cell for cell in instance.__original_cell.neighboring_cells() if not cell.is_blocked]
            
            if blocked_neighbour_cells != []:
                for cell in blocked_neighbour_cells:
                    blocked_cells_data[storage_name].pop(f'{cell.x_cell_coord}_{cell.y_cell_coord}_{cell.z_cell_coord}', None)
                    
            full_cell_info_data[instance.__original_cell.storage_name][instance.__original_cell.y_cell_coord][instance.__original_cell.x_cell_coord][instance.__original_cell.z_cell_coord] = [
            instance.__original_cell.visualization_y,
            instance.__original_cell.visualization_x,
            instance.__original_cell.visualization_z,
            instance.__original_cell.full_percent,
        ]
                
    set_cache(static_cache_keys['moving_crates'], moved_crates_data)
    set_cache(static_cache_keys['blocked_cells'], blocked_cells_data, as_list=False)
    set_cache(static_cache_keys['full_info_cells'], full_cell_info_data, as_list=False)
    
@receiver(post_save, sender=Storage)
def on_change(instance: Storage, **kwargs):
    
    data = full_cell_info()
    
    set_cache(static_cache_keys['full_info_cells'], data, as_list=False)
    
@receiver(post_delete, sender=Crates)
def on_delete(instance: Crates, **kwargs):
    
    new_cell_data = {}
    blocked_cells_data = {}
    
    if instance.cell is not None:
        new_cell_data = {
            'status': 'deleted',
            'cell_adress': instance.cell.adress,
            'storage_name': instance.cell.storage_name,
            'x_coord': instance.cell.x_cell_coord,
            'y_coord': instance.cell.y_cell_coord,
            'z_coord': instance.cell.z_cell_coord,
            'fullness':instance.cell.full_percent,
        }

        storage_name = instance.cell.storage_name
        not_blocked_neighbour_cells = [cell for cell in instance.cell.neighboring_cells() if not cell.is_blocked]

        blocked_cells_data = get_cache(static_cache_keys['blocked_cells'], {})
        full_cell_info_data = get_cache(static_cache_keys['full_info_cells'], {})
        
        if blocked_cells_data.get(storage_name, None) is not None and len(not_blocked_neighbour_cells) > 0:
            for cell in not_blocked_neighbour_cells:
                blocked_cells_data[storage_name].pop(f'{cell.x_cell_coord}_{cell.y_cell_coord}_{cell.z_cell_coord}', None)
                
        full_cell_info_data[instance.cell.storage_name][instance.cell.y_cell_coord][instance.cell.x_cell_coord][instance.cell.z_cell_coord] = [
            instance.cell.visualization_y,
            instance.cell.visualization_x,
            instance.cell.visualization_z,
            instance.cell.full_percent,
        ]
    
    set_cache(static_cache_keys['moving_crates'], new_cell_data)
    set_cache(static_cache_keys['blocked_cells'], blocked_cells_data, as_list=False)
    set_cache(static_cache_keys['full_info_cells'], full_cell_info_data, as_list=False)
    
@receiver(post_delete, sender=Storage)
def on_delete(instance: Storage, **kwargs):
    
    data = full_cell_info()
    
    set_cache(static_cache_keys['full_info_cells'], data, as_list=False)