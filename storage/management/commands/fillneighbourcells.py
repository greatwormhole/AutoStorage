from random import choice

from django.core.management import BaseCommand
from django.db import transaction

from main.models import Storage, Nomenclature, Crates
            
class Command(BaseCommand):

    help = 'Fills neighbour cells'

    def add_arguments(self, parser):
        parser.add_argument('--id', action='store', type=int)

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write('Filling...')
        
        id = kwargs['id']
        
        nomenclatures = Nomenclature.objects.all()
        cell = Storage.objects.get(adress=id)
        
        for n_cell in cell.neighboring_cells():
            n_cell.crates.all().delete()
            Crates.objects.create(
                nomenclature = choice(nomenclatures),
                amount = 1,
                size = f'{n_cell.x_cell_size}x{n_cell.y_cell_size}x{n_cell.z_cell_size}',
                cell = n_cell
            )