from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .decorators import check_access
from django.core import serializers
from .WS_cache import WS_CACHE_CONNECTION, WS_CACHE_MESSAGE
from .models import Worker, THD, Nomenclature, Crates
import random
from barcode import Code39
from .utils import CustomWriter
from transliterate import translit
import json

class HomeView(View):

    @check_access()
    def get(self, request):

        #username = json.loads(request.COOKIES.get('AccessKey')).get('name')
        username = 'ilya'
        THD_num = json.loads(request.COOKIES.get('AccessKey')).get('THD')

        if THD_num is not None:

            THD_ip = THD.objects.get(THD_number=THD_num).ip

            context = {"internalUser": username, 'THD': THD_num, 'THD_ip': THD_ip}

        else:

            context = {"internalUser": username, 'THD': THD_num}

        response = render(request, 'main/home.html', context=context)
        
        return response

class LoginView(View):

    def post(self, request):   

        request_id = request.POST.get('id', None)
        request_ip = request.POST.get('ip', None)

        if request_id is None or request_ip is None:
            return JsonResponse({'status': False, 'error': 'POST запрос составлен неверно'}, status=400)
        
        worker = Worker.objects.filter(id=request_id)
        thd = THD.objects.filter(ip=request_ip)

        if not worker:
            return JsonResponse({'status': False, 'error': 'Данного работника нет в базе'}, status=404)

        if not thd:
            return JsonResponse({'status': False, 'error': 'Данного ТСД нет в базе'}, status=404)
        
        worker = worker[0]
        thd = thd[0]

        cookie = {
            'id': int(request_id),
            'name': str(worker.name),
            'storage_right': bool(worker.storage_right),
            'plan_right': bool(worker.plan_right),
            'quality_control_right': bool(worker.quality_control_right),
            'THD': int(thd.THD_number)
        }
        data = {
            'status': True,
            'name': str(worker.name),
            'storage_right': bool(worker.storage_right),
            'plan_right': bool(worker.plan_right),
            'quality_control_right': bool(worker.quality_control_right),
        }

        thd.worker = worker
        thd.is_using = True
        thd.is_comp = False

        thd.save()
        response = JsonResponse(data, status=200)
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
            return JsonResponse({'status': False, 'error': 'GET запрос составлен неверно'}, status=400)
        
        nomenclature = Nomenclature.objects.get(article=get_article)

        if not nomenclature:
            return JsonResponse({'status': False, 'error': 'Данного артикула нет в базе'}, status=404)
        
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

        login_data = {}
        logged_in = False

        get_ip = request.META.get('REMOTE_ADDR')
        thds = THD.objects.filter(ip=get_ip)

        if not thds:
            return JsonResponse({'status': False, 'error': 'ТСД с таким ip нет в базе'}, status=404)

        thd = thds.first()
        
        if thd.worker is not None:
            login_data = {
                'status': True,
                'id': thd.worker.id,
                'name': thd.worker.name,
                'storage_right': thd.worker.storage_right,
                'plan_right': thd.worker.plan_right,
                'quality_control_right': thd.worker.quality_control_right,
            }
            logged_in = True

        return JsonResponse({'status': True, 'is_comp': thd.is_comp, 'id':thd.THD_number, 'login': login_data, 'is_logged_in': logged_in}, status=200)
    
class THDSelect(View):

    """
    View для резервирования ТСД с компьютера
    """
    def get(self, request):

        THD_ip = request.GET.get('ip')

        try:
            thd = THD.objects.get(ip=THD_ip)
        except:
            return JsonResponse({'status': False, 'error':'ТСД с таким ip нет в базе'}, status=404)
        
        thd.is_comp = False
        thd.is_using = False

        thd.save()

        return JsonResponse({}, status=200)
    
    def post(self, request):
        
        """
        Блокировка определенного ТСД за компьютером по POST запросу
        """

        THD_num = request.POST.get('THD_num')

        is_comp = request.POST.get('PC')

        try:
            thd = THD.objects.get(THD_number=THD_num)
        except:
            return JsonResponse({'status': False, 'error':'ТСД с таким ip нет в базе'}, status=404)
        
        thd.is_comp = is_comp
        thd.is_using = True

        thd.save()
        return JsonResponse({}, status=200)
    
class WebSocketTHDcheck(View):

    """
    View для реализации проверки подключения ТСД к вебсокету
    """

    def get(self, request):

        request_id = request.GET.get('id', None)

        if not request_id:
            return JsonResponse({'status': False, 'error': 'GET запрос составлен неверно'}, status=400)
        
        try:

            ip = THD.objects.get(THD_number=request_id).ip

        except:

            return JsonResponse({'status': False, 'error': 'GET запрос составлен неверно'}, status=400)

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

        request_ip = request.POST.get('ip', None)

        if not request_ip:
            return JsonResponse({'status': False, 'error': 'GET запрос составлен неверно'}, status=400)
        
        thd = THD.objects.filter(ip=request_ip)

        if not thd:
            return JsonResponse({'status': False, 'error': 'ТСД с таким ip нет в базе'}, status=404)
        
        thd = thd[0]

        if not thd.is_using:
            return JsonResponse({'status': False, 'error': 'Данное ТСД уже никем не используется'}, status=405)
        
        thd.is_comp = False
        thd.is_using = False
        thd.worker = None

        thd.save()
        response = JsonResponse({'status': True}, status=200)
        response.delete_cookie('AccessKey')

        return response
    
class CrateView(View):

    def get(self, request):

        request_crate_id = request.GET.get('id', None)

        if request_crate_id is None:
            return JsonResponse({'status': False, 'error': 'GET запрос составлен неверно'}, status=400)

        crate = Crates.objects.filter(id=request_crate_id)

        if not crate:
            return JsonResponse({'status': False, 'error': 'Коробки с таким ID нет в базе'}, status=404)
        
        crate = crate.first()

        return JsonResponse({'status': True, 'position': None}, status=200)