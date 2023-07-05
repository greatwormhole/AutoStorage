from django.shortcuts import render
from django.views import View

from barcode import Code39
from .utils import CustomWriter

from transliterate import translit

class DeliveryView(View):

    def get(self, request):
    
        article = translit('СТ-00006416', language_code='ru', reversed=True)
        nomenclature = 'Болт М5'

        ean = Code39(article, writer=CustomWriter(nomenclature))
        name = ean.save(f'media/{article}')

        context = {
            'filename': name
        }

        return render(request, 'main/barcode.html', context=context)

    def post(self, request):
        pass