from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.core import serializers
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from time import sleep

from main.decorators import check_access
from main.models import THD, Nomenclature, DeliveryNote, Worker, Crates, Storage, TempCrate, ProductionStorage
from main.utils import generate_nomenclature_barcode
from .calculate_planning import handle_calculations
from main.caching import get_cache, set_cache, static_cache_keys
from storage.management.commands.createstorage import _is_valid

import json
from datetime import datetime as dt

class main(View):
    @check_access()
    def get(self, request):

        username = json.loads(request.COOKIES.get('AccessKey')).get('name')
        THD_num = json.loads(request.COOKIES.get('AccessKey')).get('THD')
        # username = "test"
        if THD_num is not None:

            THD_ip = THD.objects.get(THD_number=THD_num).ip

            context = {"internalUser": username, 'THD': THD_num, 'THD_ip': THD_ip}

        else:

            context = {"internalUser": username, 'THD': THD_num}

        return render(request, 'storage/consignment-note.html', context=context)


class storagePlanView(View):
    @check_access()
    def get (self, request):

        username = json.loads(request.COOKIES.get('AccessKey')).get('name')
        THD_num = json.loads(request.COOKIES.get('AccessKey')).get('THD')
        # username = "test"
        if THD_num is not None:

            THD_ip = THD.objects.get(THD_number=THD_num).ip

            context = {"internalUser": username, 'THD': THD_num, 'THD_ip': THD_ip}

        else:

            context = {"internalUser": username, 'THD': THD_num}

        return render(request, 'storage/production-storage.html', context=context)

    def post(self, request):

        data = ProductionStorage.objects.all()

        response = HttpResponse(serializers.serialize('json', data), content_type='application/json')

        return response

class storageNavigation(View):
    @check_access()
    def get(self, request):

        username = json.loads(request.COOKIES.get('AccessKey')).get('name')
        THD_num = json.loads(request.COOKIES.get('AccessKey')).get('THD')
        # username = "test"
        if THD_num is not None:

            THD_ip = THD.objects.get(THD_number=THD_num).ip

            context = {"internalUser": username, 'THD': THD_num, 'THD_ip': THD_ip}

        else:

            context = {"internalUser": username, 'THD': THD_num}

        return render(request, 'storage/storage-navigation.html', context=context)

class storageVisualization(View):
    @check_access()
    def get(self, request):

        username = json.loads(request.COOKIES.get('AccessKey')).get('name')
        THD_num = json.loads(request.COOKIES.get('AccessKey')).get('THD')
        worker_id = json.loads(request.COOKIES.get('AccessKey')).get('id')
        # username = "test"
        storage_list = list(set(list(Storage.objects.values_list('storage_name',flat=True))))
        count_cell_list = []
        for i in range(len(storage_list)):
            count_cell_list.append(Storage.objects.filter(storage_name=storage_list[i]).order_by('-x_cell_coord')[0].x_cell_coord)
        for i in range(len(storage_list) - 1):
            for j in range(len(storage_list) - i - 1):
                if count_cell_list[j] > count_cell_list[j + 1]:
                    count_cell_list[j], count_cell_list[j + 1] = count_cell_list[j + 1],count_cell_list[j]
                    storage_list[j], storage_list[j + 1] = storage_list[j + 1], storage_list[j]
        if THD_num is not None:

            THD_ip = THD.objects.get(THD_number=THD_num).ip

            context = {"internalUser": username, 'THD': THD_num, 'THD_ip': THD_ip, 'storage_list':storage_list, 'worker_id': worker_id}

        else:

            context = {"internalUser": username, 'THD': THD_num}

        return render(request, 'storage/visualization.html', context=context)


class storageInfo(View):

    def get(self, request):
        
        cached = get_cache(static_cache_keys['full_info_cells'], None)
        
        # if cached is not None:
        #     return JsonResponse(data=cached, status=200)
        
        storage_names = Storage.objects.all().values_list('storage_name', flat=True).distinct()
        data = {}
        
        for storage_name in storage_names:
            
                storage = Storage.objects.filter(storage_name=storage_name)
                y_of_storage = list(storage.values_list('y_cell_coord', flat=True).distinct().order_by('y_cell_coord'))
                x_of_storage = list(storage.values_list('x_cell_coord', flat=True).distinct().order_by('x_cell_coord'))
                z_of_storage = list(storage.values_list('z_cell_coord', flat=True).distinct().order_by('z_cell_coord'))
                
                for y in y_of_storage:
                    for x in x_of_storage:
                        for z in z_of_storage:
                            print(y, x, z)
                            # sleep(1)
                            
                            if data.get(storage_name, None) is None:
                                data[storage_name] = []
                            if len(data[storage_name]) <= y:
                                data[storage_name].append([])
                            try:
                                cell = storage.get(
                                    Q(x_cell_coord=x) &
                                    Q(y_cell_coord=y) &
                                    Q(z_cell_coord=z) &
                                    Q(storage_name=storage_name)
                                )
                            except ObjectDoesNotExist:
                                data[storage_name][y].append(None)
                            # print(data[storage_name][y])
                            if len(data[storage_name][y]) <= x:
                                data[storage_name][y].append([])
                            if data[storage_name][y][-1] is None:
                                continue
                            if len(data[storage_name][y][x]) <= z:
                                data[storage_name][y][x].append([])
                            data[storage_name][y][x][z].append([cell.visualization_y, cell.visualization_x, cell.visualization_z, cell.full_percent])
        
        # data = {
        #     storage_name: {
        #         y: {
        #             x: {
        #                 z: [
        #                     cell.visualization_y,
        #                     cell.visualization_x,
        #                     cell.visualization_z,
        #                     cell.full_percent,
        #                 ]
        #                 for z in [*map(lambda i: i[2], coords)]
        #                 if (cell := storage.get(
        #                     Q(x_cell_coord=x) &
        #                     Q(y_cell_coord=y) &
        #                     Q(z_cell_coord=z) &
        #                     Q(storage_name=storage_name)
        #                 ))
        #             }
        #             for x in [*map(lambda i: i[1], coords)]
        #         }
        #         for y in [*map(lambda i: i[0], coords)]
        #     }
        #     for storage_name in storage_names
        #     if (storage := Storage.objects.filter(storage_name=storage_name)) and
        #     (coords := list(storage.values_list('y_cell_coord', 'x_cell_coord', 'z_cell_coord')))
        # }
        
        set_cache(static_cache_keys['full_info_cells'], data, as_list=False)
        
        return JsonResponse(data=data, status=200)

class NomenclatureView(View):

    """
    Получение номенклатуры по артикулу
    """

    def get(self, request):

        data = Nomenclature.objects.all()

        response = HttpResponse(serializers.serialize('json', data), content_type='application/json')
        #response.set_cookie('AccessKey', json.dumps({'id': 1}))

        return response
    
class SaveConsignmentNote(View):

    def post(self, request):

        post_data = json.loads(request.body).get('data', None)
        access_key = json.loads(request.COOKIES.get('AccessKey', None))
        request_id = access_key.get('id', None) # request.POST.get('id', None)

        if request_id is None:
            return JsonResponse({'status': False, 'error': 'POST запрос составлен неверно'}, status=400)
        
        worker = Worker.objects.filter(id=request_id)

        if not worker:
            return JsonResponse({'status': False, 'error': 'Данного работника нет в базе'}, status=404)
        
        worker = worker[0]

        consignment_note_body = f"""{post_data.get('dataCreates')}"""

        if consignment_note_body == '[]':
            return JsonResponse({'status': False, 'error': 'Пустая накладная!'}, status=404)

        worker = Worker.objects.get(id=request_id)
        delivery_note = DeliveryNote.objects.create(
            worker = worker,
            number = post_data.get('number'),
            datetime = dt.strptime(post_data.get('datetime'), '%d.%m.%Y %H:%M:%S'),
            provider = post_data.get('provider'),
            article_list = consignment_note_body
        )

        delivery_note.save()

        return HttpResponse(status=200)


class defectiveProductCreate(View):

    def get(self, request):
        username = json.loads(request.COOKIES.get('AccessKey')).get('name')
        THD_num = json.loads(request.COOKIES.get('AccessKey')).get('THD')
        if THD_num is not None:

            THD_ip = THD.objects.get(THD_number=THD_num).ip

            context = {"internalUser": username, 'THD': THD_num, 'THD_ip': THD_ip}

        else:

            context = {"internalUser": username, 'THD': THD_num}
        return render(request, 'storage/defective-product-add.html', context=context)
    
class SaveCrateView(View):
    def get(self,request):

        article = request.GET.get('data')

        box_list = Crates.objects.filter(nomenclature=Nomenclature.objects.get(article=article))

        response = HttpResponse(serializers.serialize('json', box_list), content_type='application/json')

        return response
    def post(self, request):

        data = json.loads(request.body).get('data')

        nomenclature = Nomenclature.objects.get(article=data.get('articule'))

        crate = Crates.objects.create(
            amount = data.get('count'),
            size = data.get('dimensions'),
            nomenclature = nomenclature,
        )
        crate.save()

        generate_nomenclature_barcode(crate.text_id, crate.nomenclature.title)

        return HttpResponse(status=200)
    
class SaveTempCrateView(View):
    
    def post(self, request):

        data = json.loads(request.body).get('data')
        print(data)
        crate = Crates.objects.get(id=int(data.get('id')))

        temp_crate = TempCrate.objects.create(
            crate = crate,
            amount = data.get('count'),
            size = data.get('dimensions'),
        )
        temp_crate.save()

        generate_nomenclature_barcode(temp_crate.text_id, crate.text_id)

        return HttpResponse(status=200)
    
class NomenclatureCratesView(View):

    def get(self, request):

        request_article = request.GET.get('articule', None)

        nomenclature = Nomenclature.objects.get(article=request_article)
        # print(Nomenclature.objects.get(title=))

        crates_per_nomenclature = Crates.objects.filter(nomenclature=nomenclature)

        return HttpResponse(
            serializers.serialize('json', crates_per_nomenclature),
            content_type='application/json',
            status=200
        )
    
class CratePositioningView(View):

    def post(self, request):

        crate_geometry = None
        request_crate_id = json.loads(request.body).get('id', None)

        if request_crate_id is None:
            return JsonResponse({'status': False, 'error': 'POST запрос составлен неверно'}, status=400)
        
        new_crate = Crates.objects.filter(text_id=request_crate_id)

        if not new_crate:
            return JsonResponse({'status': False, 'error': 'Коробки с таким id нет в базе'})
        
        new_crate = new_crate.first()

        # Id ячеек с коробками с одинаковой номенклатурой
        same_nom_cells = Crates.objects.\
            get(text_id=request_crate_id).\
            get_same_nomenclature().values('cell_id').\
            distinct()
        
        # Список доступных ячеек в убывающем порядке
        cells = sorted(
            [
                available_cell for cell_dct in filter(lambda celldct: celldct['cell_id'] is not None, same_nom_cells)
                if (available_cell := Storage.objects.get(adress=cell_dct['cell_id'])) # Задаем локальную переменную внутри list comrehension
                if available_cell.size_left > new_crate.volume # Добавляем ячейку в список только если объем коробки меньше свободного объема ячейки
            ],
            key=lambda cell: cell.size_left,
            reverse=True # Изменить этот параметр, если нужно заполнять сначала самые загруженные
        )

        # Цикл while чтобы найти место в ячейках с одинаковой номенклатурой пока есть подходящие ячейки
        while cells != []:
            cell = cells.pop()
            crate_geometry = handle_calculations(
                cell=cell,
                crates=list(cell.crates.all()) + [new_crate]
                )

            # Выйти из цикла если место было найдено
            if crate_geometry is not None:
                return JsonResponse(
                    data=crate_geometry,
                    status=200,
            )

        # Если мы не нашли подходящую ячейку
        # попытаемся найти ячейку в общей базе данных
        all_cells = sorted(
            [
                cell for cell in Storage.objects.all()
                if cell.size_left > new_crate.volume
            ],
            key=lambda cell: cell.size_left,
            reverse=True # Изменить этот параметр, если нужно заполнять сначала самые загруженные
        )

        # Пока не нашли нужную ячейку
        while crate_geometry is None:
            if all_cells == []:
                return JsonResponse({'status': False, 'error': 'Нет подходящих ячеек для размещения коробки'})
            cell = all_cells.pop()
            crate_geometry = handle_calculations(
                cell=cell,
                crates=list(cell.crates.all()) + [new_crate]
            )
        
        return JsonResponse(
            data=crate_geometry,
            status=200,
        )
        
class AllStorageList(View):
    
    def get(self, request):
        
        storage_names = Storage.objects.all().values_list('storage_name', flat=True).distinct()
        
        data = {
            storage_name: {
                f'{cell.x_cell_coord}_{cell.y_cell_coord}_{cell.z_cell_coord}': getColor([96, 255, 68],[255,0,0],cell.full_percent)
                for cell in storage
            }
            for storage_name in storage_names
            if (storage := Storage.objects.filter(storage_name=storage_name))
        }
        
        return JsonResponse(data=data, status=200)

def getColor(first, second, percent):
        if percent > 100:
            return [255,0,0,100]
        delta = [second[i] - first[i] for i in range(len(first))]
        color = [first[i] + list(map(lambda x: x * percent / 100, delta))[i] for i in range(len(first))]
        color.append(percent)
        return color
    
class BlockedStoragesView(View):
    
    def get(self, request):
        
        cached_blocked_cells = get_cache(static_cache_keys['blocked_cells'], None)
        
        if cached_blocked_cells is not None:
            return JsonResponse(data=cached_blocked_cells, status=200)
        
        storage_names = Storage.objects.all().values_list('storage_name', flat=True).distinct()
        
        data = {
            storage_name: {
                f'{cell.x_cell_coord}_{cell.y_cell_coord}_{cell.z_cell_coord}': cell.full_percent
                for cell in storage if cell.is_blocked
            }
            for storage_name in storage_names
            if (storage := Storage.objects.filter(storage_name=storage_name))
        }
        
        set_cache(static_cache_keys['blocked_cells'], data, as_list=False)
        
        return JsonResponse(data=data, status=200)