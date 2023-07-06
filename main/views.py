from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist, BadRequest
from django.views.decorators.csrf import csrf_exempt
from .decorators import check_access
from django.core import serializers

from .models import Worker, THD

from barcode import Code39
from .utils import CustomWriter

from transliterate import translit
import json

class base(View):

    @check_access()
    def get(self, request):

        username = json.loads(request.COOKIES.get('AccessKey')).get('name')
        context = {"internalUser": username}

        response = render(request, 'main/home.html', context=context)
        
        return response
    
    def post(self, request):
        pass

class LoginView(View):

    def get(self, request):
        
        id = request.GET.get('id')

        if id is None:
            raise BadRequest('В запросе нет id пользователя')
        
        workers = Worker.objects.filter(id=id)

        if not workers:
            raise ObjectDoesNotExist("Данного работника нет в базе")

        cookie = {
            'id': id,
            'name': str(workers[0].name),
            'storage_right': bool(workers[0].storage_right),
            'plan_right': bool(workers[0].plan_right),
            'quality_control_right': bool(workers[0].quality_control_right),
        }

        response = redirect('base')
        response.set_cookie(key='AccessKey', value=json.dumps(cookie))
        
        return response

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

class THDList(View):

    model = THD

    def get(self, request):
        
        data = THD.objects.all()

        response_json = serializers.serialize('json', data)

        return HttpResponse(response_json, content_type='application/json')