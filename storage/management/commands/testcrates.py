from random import choice
import numpy as np

from django.core.management import BaseCommand
from django.db import transaction

from main.factories import CrateFactory
from main.models import Storage, Nomenclature
from storage.calculate_planning import handle_calculations

sim_num = 5
crates_per_storage = 30
test_storage_id = 6899

crate_sizes = [*range(300, 501, 5)]

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
        
        size_left = []
        nomenclatures = Nomenclature.objects.all()
        storage = Storage.objects.get(adress=test_storage_id)
        
        for _ in range(sim_num):
            
            storage.crates.all().delete()
            crates = []
            
            for __ in range(crates_per_storage):
                crate = CrateFactory(
                    nomenclature = choice(nomenclatures),
                    size = concat_sizes(crate_sizes),
                    cell = storage,
                )
                
                if storage.size_left > crate.volume:
                    crates.append(crate)
                else:
                    storage.crates.get(id=crate.id).delete()
                    break
            
            res = handle_calculations(
                cell=storage,
                crates=crates
            )
            # print(len(storage.crates.all()))
            # print(storage.size_left)
            size_left.append(storage.size_left)
            
        mean_size_left = np.mean(size_left)
        
        self.stdout.write(f'Mean size left: {mean_size_left}')