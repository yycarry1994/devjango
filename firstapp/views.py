from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
import json
from .models import Teacher, Kecheng, Student, Source
import uuid


# Create your views here.


class AddStudent(View):
    """
    向数据库学生表添加数据
    body格式：
    {
        "name":"张三",
        "age":25,
        "sex":"男"
    }
    """
    def post(self, request):
        s_uuid = str(uuid.uuid1()).replace('-', '')
        body = json.loads(request.body)
        c_name = body.get('name')
        c_age = body.get('age')
        c_sex = body.get('sex')
        try:
            add_student = Student.objects.create(c_bh=s_uuid, c_name=c_name, c_age=c_age, c_sex=c_sex)
            return HttpResponse({'msg', '成功'}, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse(e, content_type='application/json', status=200)


class AddTeacher(View):
    """
    向数据库教师表添加数据
    body格式：
    {
        "name": "李三",
        "age": 25,
        "sex": "男",
        "kecheng": "语文"
    }
    """
    def post(self, request):
        t_uuid = str(uuid.uuid1()).replace('-', '')
        body = json.loads(request.body)
        c_name = body.get('name')
        c_age = body.get('age')
        c_sex = body.get('sex')
        c_kecheng = body.get('kecheng')
        c_x_kecheng = Kecheng.objects.get(c_xueke=c_kecheng)
        try:
            add_teacher = Teacher.objects.create(c_bh=t_uuid, c_name=c_name, c_x_bh=c_x_kecheng, n_age=c_age, c_sex=c_sex)
            return HttpResponse({'msg', '成功'}, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse(e, content_type='application/json', status=200)


class AddKecheng(View):
    """
    向数据库课程表添加数据
    body格式：
    {
        "kecheng": "语文",
    }
    """
    def post(self, request):
        body = json.loads(request.body)
        c_kecheng = body.get('kecheng')
        try:
            add_kecheng = Kecheng.objects.create(c_xueke=c_kecheng)
            return HttpResponse({'msg', '成功'}, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse(e, content_type='application/json', status=200)


class AddSource(View):
    """
    向数据库分数表添加数据
    body格式：
    {
        "fenshu": 98,
        "kecheng": '语文',
        "name": "张三"
    }
    """
    def post(self, request):
        body = json.loads(request.body)
        c_fenshu = body.get('fenshu')
        c_kecheng = body.get('kecheng')
        c_name = body.get('name')
        c_x_bh = Kecheng.objects.get(c_xueke=c_kecheng)
        c_s_bh = Student.objects.get(c_name=c_name)
        try:
            add_source = Source.objects.create(c_fenshu=c_fenshu, c_x_bh=c_x_bh, c_s_bh=c_s_bh)
            return HttpResponse({'msg', '成功'}, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse(e, content_type='application/json', status=200)

def index1(request):
    if request.method == 'GET':
        return render(request, 'test.html')
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

    def post(self, request):
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
