from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from main.models import Storage

def full_cell_info():
    
    storage_names = Storage.objects.all().values_list('storage_name', flat=True).distinct()
    data = {}

    for storage_name in storage_names:
        
        storage = Storage.objects.filter(storage_name=storage_name)
        y_of_storage = list(storage.values_list('y_cell_coord', flat=True).distinct().order_by('y_cell_coord'))
        x_of_storage = list(range(max(list(storage.values_list('x_cell_coord', flat=True))) + 1))
        z_of_storage = list(storage.values_list('z_cell_coord', flat=True).distinct().order_by('z_cell_coord'))
        
        if data.get(storage_name, None) is None:
            data[storage_name] = []
        
        for y in y_of_storage:
            if len(data[storage_name]) <= y:
                data[storage_name].append([])
            
            for x in x_of_storage:
                
                tmp = storage.filter(
                    Q(x_cell_coord=x) &
                    Q(y_cell_coord=y) &
                    Q(storage_name=storage_name)
                )
                
                if list(tmp) == []:
                    data[storage_name][y].append(None)
                    continue
                else:
                    data[storage_name][y].append([])
                
                for z in z_of_storage:
                    if len(data[storage_name][y][x]) <= z:
                        data[storage_name][y][x].append([])
                    try:
                        cell = tmp.get(z_cell_coord=z)
                    except ObjectDoesNotExist:
                        data[storage_name][y][x][z].append(None)
                    data[storage_name][y][x][z].append([cell.visualization_y, cell.visualization_x, cell.visualization_z, cell.full_percent])
        
        # data = {
        #     storage_name: {
        #         y: {
        #             x: {
        #                 z: [
        #                     cell.visualization_y,
        #                     cell.visualization_x,
        #                     cell.visualization_z,
        #                     cell.full_percent,
        #                 ]
        #                 for z in [*map(lambda i: i[2], coords)]
        #                 if (cell := storage.get(
        #                     Q(x_cell_coord=x) &
        #                     Q(y_cell_coord=y) &
        #                     Q(z_cell_coord=z) &
        #                     Q(storage_name=storage_name)
        #                 ))
        #             }
        #             for x in [*map(lambda i: i[1], coords)]
        #         }
        #         for y in [*map(lambda i: i[0], coords)]
        #     }
        #     for storage_name in storage_names
        #     if (storage := Storage.objects.filter(storage_name=storage_name)) and
        #     (coords := list(storage.values_list('y_cell_coord', 'x_cell_coord', 'z_cell_coord')))
        # }
        
    return data