from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .decorators import check_access
from django.core import serializers
from .WS_cache import WS_CACHE_CONNECTION, WS_CACHE_MESSAGE
from .models import Worker, THD, Nomenclature
import random
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

class LoginView(View):

    def get(self, request):
        
        get_id = request.GET.get('id', None)

        if get_id is None:
            return JsonResponse({'status': False, 'error': 'GET запрос составлен неверно'}, status=400)
        
        worker = Worker.objects.get(id=get_id)

        if not worker:
            return JsonResponse({'status': False, 'error': 'Данного работника нет в базе'}, status=404)

        cookie = {
            'id': int(get_id),
            'name': str(worker.name),
            'storage_right': bool(worker.storage_right),
            'plan_right': bool(worker.plan_right),
            'quality_control_right': bool(worker.quality_control_right),
        }

        response = JsonResponse({'status': True, 'name': cookie.get('name')}, status=200)
        response.set_cookie(key='AccessKey', value=json.dumps(cookie))
        
        return response

class DeliveryView(View):

    """
    Генерация накладной
    """

    @check_access()
    def get(self, request):
    
        article = translit('22222222', language_code='ru', reversed=True)
        print(article)
        nomenclature = 'Болт М5'

        ean = Code39(article, writer=CustomWriter(nomenclature), add_checksum=False)
        name = ean.save(f'media/{article}')

        context = {
            'filename': name
        }

        return render(request, 'main/barcode.html', context=context)

class THDList(View):

    @check_access()
    def get(self, request):
        
        data = THD.objects.all()

        response_json = serializers.serialize('json', data)

        return HttpResponse(response_json, content_type='application/json')
    
class NomenclatureView(View):

    @check_access()
    def get(self, request):
        
        get_article = request.GET.get('article', None)

        if get_article is None:
            return JsonResponse({'error': 'GET запрос составлен неверно'}, status=400)
        
        nomenclature = Nomenclature.objects.get(article=get_article)

        if not nomenclature:
            return JsonResponse({'error': 'Данного артикула нет в базе'}, status=404)
        
        data = {
            'nomenclature': nomenclature.title,
            'units': nomenclature.units,
            'mass': nomenclature.mass
        }

        response = JsonResponse(data=data)

        return response
    
class MainView(View):
    
    """
    View для резервирования ТСД
    """

    def get(self, request):

        """
        Проверка по GET запросу является ли авторизация с компьютера или с ТСД,
        необходима для отправки на ТСД информации отображения определенного экрана
        """

        get_ip = request.META.get('REMOTE_ADDR')
        thd = THD.objects.get(ip=get_ip)

        if not thd:
            return JsonResponse(data ={'error': 'ТСД с таким ip нет в базе'}, status=404)

        return JsonResponse(data={'is_comp': thd.is_comp, 'id':thd.THD_number}, status=200)

    # def post(self, request):
        
    #     """
    #     Блокировка ТСД с определнным id в базе по POST запросу
    #     """

    #     get_ip = request.META.get('REMOTE_ADDR')
    #     thd = THD.objects.get(ip=get_ip)

    #     if not thd:
    #         return JsonResponse(data = {'error': 'ТСД с таким ip нет в базе'}, status=404)

    #     if thd.is_using:
    #         return JsonResponse({'error': 'Данное устройство уже занято'}, status=403)
        
    #     thd.is_using = True
    #     thd.save()

    #     return JsonResponse({'status': True})
    

class THDSelect(View):

    """
    View для резервирования ТСД с компьютера
    """

    def post(self, request):
        
        """
        Блокировка определенного ТСД за компьютером по POST запросу
        """

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
    
class WebSocketTHDcheck(View):

    """
    View для реализации проверки подключения ТСД к вебсокету
    """

    def get(self, request):

        request_id = request.GET.get('id', None)
        print(WS_CACHE_CONNECTION)
        if not request_id:
            return JsonResponse({'error': 'GET запрос составлен неверно'}, status=400)
        try:

            ip = THD.objects.get(THD_number=request_id).ip

        except:

            return JsonResponse({'error': 'GET запрос составлен неверно'}, status=400)

        if ip not in WS_CACHE_CONNECTION.keys():

            return JsonResponse({'status': False}, status=200)

        if WS_CACHE_CONNECTION[ip]:

            return JsonResponse({'status': True}, status=200)

        else:

            return JsonResponse({'status': False}, status=200)


class LogoutView(View):

    """
    View для реализации выхода пользователя из системы
    """

    def post(self, request):

        request_id = request.POST.get('id', None)

        if not request_id:
            return JsonResponse({'error': 'GET запрос составлен неверно'}, status=400)
        
        try:
            thd = THD.objects.get(id=request_id)
        except:
            return JsonResponse(data={'error':'ТСД с таким ip нет в базе'}, status=404)
        
        thd.is_comp = False
        thd.is_using = False

        thd.save()
        response = JsonResponse({'status': True}, status=200)
        response.delete_cookie('AccessKey')

        return response