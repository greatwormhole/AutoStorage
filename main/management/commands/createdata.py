import random

from django.core.management import BaseCommand
from django.db import transaction

from main.factories import *

CRATE_NUM = 10
WORKER_NUM = 10
NOMENCLATURE_NUM = 20
CELLS_PER_STORAGE = 5
STORAGE_NUM = 5

STORAGES = [f'Склад {i}' for i in range(1, STORAGE_NUM + 1)]
UNITS = ['шт', 'кг']
crate_sizes = [1500, 1500, 1500]

class Command(BaseCommand):

    help = 'Generates fake data'

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write('Creating new data...')

        storage_cells = Storage.objects.all()

        # storage_cells = [StorageFactory(
        #     storage_name = random.choice(STORAGES)
        # ) for storage in range(STORAGE_NUM) for _ in range(CELLS_PER_STORAGE)]
        # workers = [WorkerFactory() for _ in range(WORKER_NUM)]
        nomenclatures = [NomenclatureFactory(
            units = random.choice(UNITS)
        ) for _ in range(NOMENCLATURE_NUM)]

        crates = [Crates.objects.create(
             nomenclature = random.choice(nomenclatures),
             amount=1,
             size = f'{random.choice(crate_sizes)}x{random.choice(crate_sizes)}x{random.choice(crate_sizes)}',
             cell = random.choice(storage_cells)
         ) for _ in range(CRATE_NUM)]