from random import choice

from django.test import TestCase, Client

from main.models import Storage, Crates
from main.factories import NomenclatureFactory
from main.caching import get_cache, delete_cache_from_dict, static_cache_keys

UNITS = ['шт', 'кг']
NOMENCLATURE_NUM = 20
STORAGE_NAMES = ['TEST_1', 'TEST_2', 'TEST 3']

class BlockedCellsTestCase(TestCase):
    
    def setUp(self):
        
        self.client = Client()
        
        nomenclatures = [NomenclatureFactory(
            units = choice(UNITS)
        ) for _ in range(NOMENCLATURE_NUM)]
        
        for i in range(3):
            for j in range(3):
                cell = Storage.objects.get_or_create(
                    adress = i * 3 + j,
                    x_cell_size = 1000,
                    y_cell_size = 1000,
                    z_cell_size = 1000,
                    x_cell_coord = 14+i,
                    y_cell_coord = 14+j,
                    z_cell_coord = 1,
                    storage_name = STORAGE_NAMES[0]
                )
                Crates.objects.create(
                    nomenclature = choice(nomenclatures),
                    amount = 100,
                    size = '950x950x950',
                    cell = cell[0]
                )
        
    def tests_run(self):
        self.Test_blocked()
        self.Test_cached()
        
    def Test_blocked(self):
        blocked_cells = self.client.get('/API/check-blocked-cells').json()
        self.assertEqual(blocked_cells, {STORAGE_NAMES[0]: {'15_15_1': 86}})
        
    def Test_cached(self):
        cached = get_cache(static_cache_keys['blocked_cells'], None)
        self.assertIsNotNone(cached, 'Cache has not been written')
        delete_cache_from_dict(static_cache_keys['blocked_cells'], STORAGE_NAMES[0])