from random import choice

from django.core.management import BaseCommand
from django.db import transaction

from main.factories import *
from main.models import Storage

sizes = [1000, 2000, 3000]

x_storage_size = 50
y_storage_size = 50
z_storage_size = 3

x_gap_size = 10
y_gap_size = 20

def _is_valid(x, y, z = None):
    
    x_start_coord = (x_storage_size - x_gap_size) // 2
    y_start_coord = (y_storage_size - y_gap_size)
    
    return (x not in range(x_start_coord, x_start_coord + x_gap_size),
            y not in range(y_start_coord, y_start_coord + y_gap_size))
            
class Command(BaseCommand):

    help = 'Generates fake data'

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write('Creating storage...')
        
        storage_cells = [
            StorageFactory(
                x_cell_size = choice(sizes),
                y_cell_size = choice(sizes),
                z_cell_size = choice(sizes),
                x_cell_coord = x,
                y_cell_coord = y,
                z_cell_coord = z,
                storage_name = 'ЦМС',
            )
            for x in range(x_storage_size)
            for y in range(y_storage_size)
            for z in range(z_storage_size)
            if True in _is_valid(x, y)
        ]
        
        self.stdout.write(f'Number of cells: {len(storage_cells)}')