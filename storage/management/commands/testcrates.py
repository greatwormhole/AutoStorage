from random import choice
import numpy as np
from time import time

from django.core.management import BaseCommand
from django.db import transaction

from main.models import Storage, Nomenclature, Crates
from storage.calculate_planning import handle_calculations
from storage.rand_boxes import Box, Cell

sim_num = 10
crates_per_storage = 20
test_storage_id = 6899

crate_sizes = [*range(400, 1000, 100)]

amounts = [1]

def concat_sizes(available_sizes: list):
    return f'''
            {choice(available_sizes)}x
            {choice(available_sizes)}x
            {choice(available_sizes)}
            '''

class Command(BaseCommand):

    help = 'Generates fake data'

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write('Testing crate disposition...')
        
        start = time()
        counter = 1
        failure_counter = 0
        res = []
        res_rand = []
        nomenclatures = Nomenclature.objects.all()
        storage = Storage.objects.get(adress=test_storage_id)
        storage_WHD = (storage.x_cell_size, storage.y_cell_size, storage.z_cell_size)
        storage.crates.all().delete()
        
        for _ in range(sim_num):
            
            self.stdout.write(f'Iteration #{counter}')
            
            crates = []
            
            for __ in range(crates_per_storage):
                crate = Crates.objects.create(
                    nomenclature = choice(nomenclatures),
                    size = concat_sizes(crate_sizes),
                    cell = storage,
                    amount=choice(amounts)
                )
                
                if storage.size_left > crate.volume:
                    crates.append(crate)
                else:
                    storage.crates.get(id=crate.id).delete()
                    break

            algorithm_res = handle_calculations(
                cell=storage,
                crates=crates,
                show_volume_left=True
            )
            
            rand_cell = Cell(storage_WHD)
            rand_cell.generate_boxes(crates_per_storage, crate_sizes, 3000)
            res_rand.append((rand_cell.vol_left, len(rand_cell.boxes)))
            
            if algorithm_res is not None:
                res.append(algorithm_res)
            else:
                failure_counter += 1
                
            storage.crates.all().delete()
            counter += 1

        mean_size_left = np.mean([i[0] for i in res])
        mean_size_left_rand = np.mean([i[0] for i in res_rand])
        
        mean_crates_packed = np.mean([i[1] for i in res])
        mean_crates_packed_rand = np.mean([i[1] for i in res_rand])
        
        end = time()
        
        self.stdout.write(
            f'''
Mean size left with packing algorithm: {round(mean_size_left / 1000000000, 3)} m^3, 
Without packing algorithm: {round(mean_size_left_rand / 1000000000, 3)} m^3,
algorithm runtime: {round(end - start, 2)} s, 
algorithm failed {failure_counter} attempts out of {sim_num};
Algorithm has packed {round(mean_crates_packed)} crates while random disposition packed {round(mean_crates_packed_rand)}.
Algorithm is better by {round((mean_crates_packed - mean_crates_packed_rand) / mean_crates_packed_rand * 100, 2)}%.
''')