import random

from django.core.management import BaseCommand
from django.db import transaction

from main.factories import *

CRATE_NUM = 100
WORKER_NUM = 20
NOMENCLATURE_NUM = 1000
CELLS_PER_STORAGE = 20
STORAGE_NUM = 5

STORAGES = [f'Склад {i}' for i in range(1, STORAGE_NUM + 1)]
UNITS = ['шт', 'кг']

class Command(BaseCommand):

    help = 'Generates fake data'

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write('Creating new data...')

        storage_cells = [StorageFactory(
            storage_name = random.choice(STORAGES)
        ) for storage in range(STORAGE_NUM) for _ in range(CELLS_PER_STORAGE)]
        workers = [WorkerFactory() for _ in range(WORKER_NUM)]
        nomenclatures = [NomenclatureFactory(
            units = random.choice(UNITS)
        ) for _ in range(NOMENCLATURE_NUM)]

        crates = [CrateFactory(
            nomenclature = random.choice(nomenclatures),
            cell = random.choice(storage_cells)
        ) for _ in range(CRATE_NUM)]