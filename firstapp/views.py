from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
import json
# Create your views here.


def index1(request):
    if request.method == 'GET':
        return render('test.html', 'test.html')
    elif request.method == 'POST':
        return HttpResponse('hello world')


class index2(View):
    """
    类视图
    """
    def get(self, request):
        data = {
            "methed": "get",
            "name": "yangyang",
            "age": "18"
        }
        data = json.dumps(data, ensure_ascii=False)
        return HttpResponse(data, content_type='application/json', status=200)

    def psot(self, request):
        data = {
            "methed": "post",
            "name": "yangyang",
            "age": "18"
        }
        data = json.dumps(data, ensure_ascii=False)
        return HttpResponse(data, content_type='application/json', status=200)

    def delete(self, request):
        data = {
            "methed": "delete",
            "name": "yangyang",
            "age": "18"
        }
        return JsonResponse(data, safe=False)
        # data = json.dumps(data, ensure_ascii=False)
        # return HttpResponse(data, content_type='application/json', status=200)


