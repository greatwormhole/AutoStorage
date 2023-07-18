from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction
from main.models import Storage, Worker, Nomenclature, Crates

class Command(BaseCommand):

    help = 'Deletes fake data'

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write("Deleting old data...")

        models = apps.get_models()

        for m in models:
            if issubclass(m, Worker) or issubclass(m, Storage) or issubclass(m, Nomenclature) or issubclass(m, Crates):
                m.objects.all().delete()
        


