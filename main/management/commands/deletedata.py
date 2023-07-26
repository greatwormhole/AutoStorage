from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction
from main.models import Storage, Worker, Nomenclature, Crates, DeliveryNote, ProductionStorage

class Command(BaseCommand):

    help = 'Deletes fake data'

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write("Deleting old data...")

        #Crates.objects.all().delete()
        #Worker.objects.all().delete()
        #Nomenclature.objects.all().delete()
        #Storage.objects.all().delete()
        #DeliveryNote.objects.all().delete()
        ProductionStorage.objects.all().delete()