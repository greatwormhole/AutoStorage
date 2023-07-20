from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.core import serializers

from main.models import THD, Nomenclature, DeliveryNote, Worker

import json
from datetime import datetime as dt

class main(View):

    def get(self, request):

        username = json.loads(request.COOKIES.get('AccessKey')).get('name')
        THD_num = json.loads(request.COOKIES.get('AccessKey')).get('THD')
        #username = "test"
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