from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.core import serializers

from main.models import THD, Nomenclature, DeliveryNote, Worker, Crates, Storage
from main.utils import generate_nomenclature_barcode
from .calculate_planning import handle_calculations

import json
from datetime import datetime as dt

class main(View):

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
        worker = Worker.objects.get(id=request_id)
        delivery_note = DeliveryNote.objects.create(
            worker = worker,
            id = post_data.get('number'),
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

        crate = Crates.objects.get(text_id=data.get('id'))

        temp_crate = Crates.objects.create(
            amount = data.get('count'),
            size = data.get('dimensions'),
            nomenclature = crate.nomenclature,
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

        crate_geomentry = None
        request_crate_id = request.POST.get('id', None)

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
                available_cell for cell_dct in same_nom_cells
                if (available_cell := Storage.objects.get(adress=cell_dct['cell_id'])) # Задаем локальную переменную внутри list comrehension
                if available_cell.size_left > new_crate.volume # Добавляем ячейку в список только если объем коробки меньше свободного объема ячейки
            ],
            key=lambda cell: cell.size_left,
            reverse=True
        )

        # Цикл while чтобы найти место в ячейках с одинаковой номенклатурой пока есть подходящие ячейки
        while cells != []:
            print(cells)
            cell = cells.pop()
            crate_geomentry = handle_calculations(
                cell=cell,
                crates=list(cell.crates.all()) + [new_crate]
                )

            # Выйти из цикла если место было найдено
            if crate_geomentry is not None:
                break

        # Если мы не нашли подходящую ячейку
        # попытаемся найти ячейку в общей базе данных
        else:

            all_cells = sorted(
                [
                    cell for cell in Storage.objects.all()
                    if cell.size_left > new_crate.volume
                ],
                key=lambda cell: cell.size_left,
                reverse=True,
            )
            
            # Пока не нашли нужную ячейку
            while crate_geomentry is None:

                cell = all_cells.pop()
                print(cell)
                crate_geomentry = handle_calculations(
                    cell=cell,
                    crates=list(cell.crates.all()) + [new_crate]
                )

        return JsonResponse(
            data={'status': True, 'data': crate_geomentry},
            status=200,
        ) if crate_geomentry\
        else JsonResponse(
            data={'status': False, 'error': 'Подходящее место не было найдено'},
            status=404
        )