from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views import View
from .decorators import check_access

from .models import Worker

from barcode import Code39
from .utils import CustomWriter

from transliterate import translit
import json

class base(View):

    def get(self, request):

        id = int(request.GET.get('id'))
        workers = Worker.objects.filter(id=id)

        if not workers:
            return HttpResponseNotFound("Данного работника нет в базе")

        username = str(workers[0].name)
        context = {"internalUser": username}
        cookie = {
            'id': id,
            'storage_right': workers[0].storage_right,
            'plan_right': workers[0].plan_right,
            'quality_control_right': workers[0].quality_control_right,
        }

        response = render(request, 'main/home.html', context=context)
        response.set_cookie(key='AccessKey', value=json.dumps(cookie))
        
        return response
    
    def post(self, request):
        pass


class DeliveryView(View):

    @check_access('storage_right')
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
