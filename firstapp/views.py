from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
import json
# Create your views here.


def index1(request):
    if request.methed == 'get':
        return render('test', 'test.html')
    elif request.methed == 'post':
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


