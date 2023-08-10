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

class Command(BaseCommand):

    help = 'Generates fake data'

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write('Deleting storage...')
        
        Storage.objects.all().delete()