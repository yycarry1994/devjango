from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
import json
from .models import Teacher, Kecheng, Student, Source
import uuid
from . import serializers


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
            return HttpResponse(e, content_type='application/json', status=500)


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
            add_teacher = Teacher.objects.create(c_bh=t_uuid, c_name=c_name, c_x_bh=c_x_kecheng, n_age=c_age,
                                                 c_sex=c_sex)
            return HttpResponse({'msg', '成功'}, content_type='application/json', status=200)
        except Exception as e:
            return HttpResponse(e, content_type='application/json', status=500)


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
            return HttpResponse(e, content_type='application/json', status=500)


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
            return HttpResponse(e, content_type='application/json', status=500)


"""
一、需求：开发5个接口，前端可以对项目进行增删改查操作
1.需要能获取到项目的列数数据（获取所有数据）(改为获取课程表)
    url: /projects/
    method：GET
    response data: json
2.需要能获取到项目的详情数据（获取前端指定某一条数据）(改为获取课程表)
    url: /projects/<int:pk>/
    method：GET
    response data: json
3.能够创建项目（创建一个项目）（已实现）
    url: /projects/
    method：POST
    request data: json
    response data: json
4.能够更新项目（只更新某一个项目）（课程表）
    url: /projects/<int:pk>/
    method：PUT
    request data: json
    response data: json
5.能够删除项目（只删除某一个项目）（课程表）
    url: /projects/<int:pk>/
    method：DELETE
"""


class GetKecheng(View):
    """
    一、需求：开发5个接口，前端可以对项目进行增删改查操作
    """

    def get_obj(self, pk):
        try:
            return Kecheng.objects.get(c_bh=pk)
        except Exception:
            raise Http404

    def get(self, request):
        """
        1.需要能获取到项目的列数数据（获取所有数据）(改为获取课程表)
        url: /projects/      (/kechengs/)
        method：GET
        response data: json
        """
        the_xueke = Kecheng.objects.all()
        num_the_xueke = the_xueke.count()
        the_data = serializers.KechengSerializer(instance=the_xueke, many=True).data
        data = {
            "msg": "成功",
            "num": num_the_xueke,
            "kecheng": the_data
        }
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False}, safe=False, status=200)

    def post(self, request):
        """
        3.能够创建项目（创建一个项目）（已实现）
        url: /projects/    (/kechengs/)
        method：POST
        request data: json
        response data: json
        body格式：
        {
            "kecheng": "语文",
        }
        """
        body = json.loads(request.body.decode('utf-8'))
        serializer_obj = serializers.KechengSerializer(data=body)
        if not serializer_obj.is_valid():
            return_data = {
                "msg": serializer_obj.errors,
                "reason": "传入参数异常"
            }
            return JsonResponse(return_data, json_dumps_params={'ensure_ascii': False}, safe=False, status=200)
        serializer_obj.save()
        data = json.dumps(serializer_obj.data)
        return HttpResponse(data, content_type='application/json', status=200)


class DealKecheng(View):

    def get_obj(self, pk):
        try:
            return Kecheng.objects.get(c_bh=pk)
        except Exception:
            raise Http404

    def get(self, request, pk):
        """
        2.需要能获取到项目的详情数据（获取前端指定某一条数据）(改为获取课程表)
        url: /projects/<int:pk>/
        method：GET
        response data: json
        """
        the_kecheng = self.get_obj(pk)
        if isinstance(the_kecheng, Http404):
            return the_kecheng
        data = serializers.KechengSerializer(instance=the_kecheng).data
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4}, status=200)

    def put(self, request, pk):
        """
        4.能够更新项目（只更新某一个项目）（课程表）
        url: /projects/<int:pk>/
        method：PUT
        request data: json
        response data: json
        {
            "c_xueke":"测试"
        }
        """
        ret = {
            "msg": "传入参数格式不正确",
            "reason": ""
        }
        the_kecheng = self.get_obj(pk)
        if isinstance(the_kecheng, Http404):
            return the_kecheng
        body_data = request.body.decode('utf-8')
        try:
            data = json.loads(body_data)
        except json.JSONDecodeError:
            return JsonResponse({"msg": "传入参数格式不正确"}, json_dumps_params={'ensure_ascii': False, 'indent': 4}, status=400)
        serializers_kecheng = serializers.KechengSerializer(instance=the_kecheng, data=data)
        try:
             serializers_kecheng.is_valid(raise_exception=True)
        except:
            errors = serializers_kecheng.error_messages
            ret['reason'] = errors
            return JsonResponse(ret, json_dumps_params={'ensure_ascii': False, 'indent': 4}, status=400)
        serializers_kecheng.save()
        return JsonResponse(serializers_kecheng.data, json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False, status=200)

    def delete(self, request, pk):
        """
        5.能够删除项目（只删除某一个项目）（课程表）
        url: /projects/<int:pk>/
        method：DELETE
        """
        the_kecheng = self.get_obj(pk)
        if isinstance(the_kecheng, Http404):
            return the_kecheng
        the_kecheng.delete()
        return HttpResponse({'msg', '成功'}, content_type='application/json', status=200)


class DealStudent(View):

    def get_obj(self, uuid):
        try:
            return Student.objects.get(c_bh=uuid)
        except Exception:
            return Http404

    def get_uuid(self):
        return str(uuid.uuid1()).replace('-', '')

    def post(self, request):
        ret = {
            "code": "500",
            "msg": "传入参数格式不正确",
            "reason": ""
        }
        body_data = request.body.decode('utf-8')
        try:
            body_data = json.loads(body_data)
        except json.JSONDecodeError as e:
            ret["reason"] = e
            return JsonResponse(ret, json_dumps_params={'ensure_ascii': False, 'indent': 4}, status=400)
        student_serializer = serializers.StudentSerializer(data=body_data)
        try:
            student_serializer.is_valid(raise_exception=True)
        except:
            ret["reason"] = student_serializer.errors
            return JsonResponse(ret, json_dumps_params={'ensure_ascii': False, 'indent': 4}, status=400)
        student_uuid = self.get_uuid()
        student_serializer.save(c_bh=student_uuid)
        return JsonResponse(student_serializer.data, json_dumps_params={'ensure_ascii': False, 'indent': 4},
                            safe=False, status=200)

    def put(self, request):
        ret = {
            "code": "500",
            "msg": "传入参数格式不正确",
            "reason": ""
        }
        body_data = request.body.decode('utf-8')
        try:
            body_data = json.loads(body_data)
        except json.JSONDecodeError as e:
            ret["reason"] = e
            return JsonResponse(ret, json_dumps_params={'ensure_ascii': False, 'indent': 4}, status=400)
        student_uuid = body_data.get('c_bh')
        student_obj = self.get_obj(student_uuid)
        if isinstance(student_obj, Http404):
            return student_obj
        student_serializer = serializers.StudentSerializer(instance=student_obj, data=body_data)
        try:
            student_serializer.is_valid(raise_exception=True)
        except:
            return JsonResponse({"msg": "传入参数不正确"}, json_dumps_params={'ensure_ascii': False, 'indent': 4}, status=400)
        student_serializer.save(c_bh=student_uuid)
        return JsonResponse(student_serializer.validated_data, json_dumps_params={'ensure_ascii': False, 'indent': 4},
                            safe=False, status=200)


class DealTeacher(View):

    def get_obj(self, student_uuid):
        return Teacher.objects.get(c_bh=student_uuid)

    def get_uuid(self):
        return str(uuid.uuid1()).replace('-', '')

    def get(self, request):
        ret = {
            'msg': '500',
            'reason': ''
        }
        body_data = request.body.decode('utf-8')
        try:
            body_data = json.loads(body_data)
        except json.JSONDecodeError as e:
            ret["reason"] = e
            return JsonResponse(ret, json_dumps_params={'ensure_ascii': False, 'indent': 4}, status=400)
        the_teacher = self.get_obj(body_data.get('c_bh'))
        teacher_serializer = serializers.TeacherSerializer(instance=the_teacher).data
        return JsonResponse(teacher_serializer, json_dumps_params={'ensure_ascii': False, 'indent': 4}, status=400)

    def post(self, request):
        ret = {
            'msg': '500',
            'reason': ''
        }
        body_data = request.body.decode('utf-8')
        try:
            data = json.loads(body_data)
        except json.JSONDecodeError as e:
            ret["reason"] = e
            return JsonResponse(ret, json_dumps_params={'ensure_ascii': False, 'indent': 4}, status=400)
        teacher_uuid = self.get_uuid()
        teacher_serializer = serializers.TeacherSerializer(data=data)
        try:
            teacher_serializer.is_valid(raise_exception=True)
        except:
            ret['reason'] = teacher_serializer.errors
            return JsonResponse(ret, json_dumps_params={'ensure_ascii': False, 'indent': 4}, status=400)
        teacher_serializer.save(c_bh=teacher_uuid)
        return JsonResponse(teacher_serializer.data, json_dumps_params={'ensure_ascii': False, 'indent': 4},
                            safe=False, status=200)

    def put(self, request):
        ret = {
            'msg': '500',
            'reason': ''
        }
        body_data = request.body.decode('utf-8')
        try:
            body_data = json.loads(body_data)
        except json.JSONDecodeError as e:
            ret["reason"] = e
            return JsonResponse(ret, json_dumps_params={'ensure_ascii': False, 'indent': 4}, status=400)
        the_teacher = self.get_obj(body_data.get('c_bh'))
        teacher_serializer = serializers.TeacherSerializer(instance=the_teacher, data=body_data)
        try:
            teacher_serializer.is_valid(raise_exception=True)
        except:
            ret['reason'] = teacher_serializer.errors
        teacher_serializer.save()
        return JsonResponse(teacher_serializer.data, json_dumps_params={'ensure_ascii': False, 'indent': 4},
                            safe=False, status=200)


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
