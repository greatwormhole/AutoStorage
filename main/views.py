from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist, BadRequest, PermissionDenied
from .decorators import check_access
from django.core import serializers

from .models import Worker, THD, Nomenclature

from barcode import Code39
from .utils import CustomWriter

from transliterate import translit
import json

class HomeView(View):

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
        
        get_id = request.GET.get('id', None)

        if get_id is None:
            raise BadRequest('В запросе нет id пользователя')
        
        worker = Worker.objects.get(id=get_id)

        if not worker:
            raise ObjectDoesNotExist("Данного работника нет в базе")

        cookie = {
            'id': get_id,
            'name': str(worker.name),
            'storage_right': bool(worker.storage_right),
            'plan_right': bool(worker.plan_right),
            'quality_control_right': bool(worker.quality_control_right),
        }

        response = redirect('home')
        response.set_cookie(key='AccessKey', value=json.dumps(cookie))
        
        return response

class DeliveryView(View):

    @check_access()
    def get(self, request):
    
        article = translit('2222', language_code='ru', reversed=True)
        print(article)
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

    @check_access()
    def get(self, request):
        
        data = THD.objects.all()

        response_json = serializers.serialize('json', data)

        return HttpResponse(response_json, content_type='application/json')
    
    def post(self, request):
        
        thd = self.model()

    
class NomenclatureView(View):

    @check_access()
    def get(self, request):
        
        get_article = request.GET.get('article', None)

        if get_article is None:
            raise BadRequest('GET запрос составлен неверно')
        
        nomenclature = Nomenclature.objects.get(article=get_article)

        if not nomenclature:
            raise ObjectDoesNotExist('Данного артикула нет в базе')
        
        data = {
            'nomenclature': nomenclature.title,
            'units': nomenclature.units,
            'mass': nomenclature.mass
        }

        response = JsonResponse(data=data)

        return response
    
class MainView(View):
    
    def get(self, request):
        pass

    def post(self, request):
        
        get_ip = request.META.get('REMOTE_ADDR')
        thd = THD.objects.get(ip=get_ip)

        if not thd:
            raise ObjectDoesNotExist('ТСД с таким ip нет в базе')

        if thd.is_using:
            raise PermissionDenied('Данное устройство уже занято')
        
        thd.is_using = True
        thd.save()

        return JsonResponse({'status': True})
    

class THDSelect(View):

    def post(self, request):
        
        THD_num = request.POST.get('THD_num')

        is_comp = request.POST.get('PC')

        try:

            thd = THD.objects.get(THD_number=THD_num)

        except:

            return JsonResponse(data={'error':'ТСД с таким ip нет в базе'}, status=404)
        
        thd.is_comp = is_comp
        
        thd.is_using = True

        thd.save()

        return JsonResponse(data={}, status=200)