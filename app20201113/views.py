import json
import uuid

from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.response import Response
from rest_framework import status, filters

from . import serializers
from firstapp.models import Kecheng, Teacher, Student, Source
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import mixins


class HomeWork1(APIView):

    def post(self, request):
        data = request.data
        the_obj = serializers.Homework1(data=data)
        the_obj.is_valid(raise_exception=True)
        return Response(the_obj.data)


class HomeWork2(APIView):

    def post(self, request):
        data = request.data
        the_obj = serializers.Homeworks(data=data)
        the_obj.is_valid(raise_exception=True)
        return Response(the_obj.data)


class GetKecheng(GenericAPIView):
    """
    一、需求：开发5个接口，前端可以对项目进行增删改查操作
    """
    queryset = Kecheng.objects.all()
    serializer_class = serializers.KechengSerializer
    # pagination_class = ''
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['c_bh', 'c_xueke']
    search_fields = ['c_bh', 'c_xueke']
    SEARCH_PARAM = 'search'

    # def get_obj(self, pk):
    #     try:
    #         return Kecheng.objects.get(c_bh=pk)
    #     except Exception:
    #         raise Http404

    def get(self, request):
        """
        1.需要能获取到项目的列数数据（获取所有数据）(改为获取课程表)
        url: /projects/      (/kechengs/)
        method：GET
        response data: json
        """
        the_xueke = self.get_queryset()
        # param = request.query_params.get('c_xueke')
        # qs = the_xueke.filter(c_xueke__icontains=param)
        qs = self.filter_queryset(the_xueke)
        page = self.paginate_queryset(qs)
        if page:
            serializers_obj = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(serializers_obj.data)
        the_obj = self.get_serializer(instance=page, many=True)
        return Response(the_obj.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        3.能够创建项目（创建一个项目）（已实现）
        url: /projects/    (/kechengs/)
        method：POST
        request data: json
        response data: json
        body格式：
        {
            "c_xueke": "语文",
        }
        """
        body = request.data
        serializer_obj = self.get_serializer(data=body)
        serializer_obj.is_valid(raise_exception=True)
        serializer_obj.save()
        return Response(serializer_obj.data, status=status.HTTP_201_CREATED)


class DealKecheng(GenericAPIView):

    queryset = Kecheng.objects.all()
    serializer_class = serializers.KechengSerializer

    def get(self, request, pk):
        """
        2.需要能获取到项目的详情数据（获取前端指定某一条数据）(改为获取课程表)
        url: /projects/<int:pk>/
        method：GET
        response data: json
        """
        the_kecheng = self.get_object()
        the_onj = self.get_serializer(instance=the_kecheng)
        return Response(the_onj.data, status=status.HTTP_200_OK)

    def put(self, request):
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
        the_kecheng = self.get_object()
        the_obj = self.get_serializer(instance=the_kecheng, data=request.data)
        the_obj.is_valid(raise_exception=True)
        the_obj.save()
        return Response(the_obj.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        """
        5.能够删除项目（只删除某一个项目）（课程表）
        url: /projects/<int:pk>/
        method：DELETE
        """
        the_kecheng = self.get_object()
        the_kecheng.delete()
        return Response({'msg', '成功'}, status=status.HTTP_204_NO_CONTENT)


class DealStudent(GenericAPIView):

    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer

    def get_uuid(self):
        return str(uuid.uuid1()).replace('-', '')

    def post(self, request):
        the_obj = self.get_serializer(data=request.data)
        the_obj.is_valid(raise_exception=True)
        student_uuid = self.get_uuid()
        the_obj.save(c_bh=student_uuid)
        return Response(the_obj.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        body_data = request.data
        student_uuid = body_data.get('c_bh')
        student_obj = self.get_queryset()
        student_obj = student_obj.get(c_bh=student_uuid)
        the_obj = self.get_serializer(instance=student_obj, data=body_data)
        the_obj.is_valid(raise_exception=True)
        the_obj.save(c_bh=student_uuid)
        return Response(the_obj.data, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class GetStudent(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
    # lookup_field = 'c_bh'

    def get_uuid(self):
        return str(uuid.uuid1()).replace('-', '')

    def get(self, request, pk):
        # lookup_field = 'cbh'
        student_obj = self.get_object()
        the_obj = self.get_serializer(instance=student_obj)
        return Response(the_obj.data, status=status.HTTP_200_OK)


class DealTeacher(GenericAPIView):

    queryset = Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer

    # def get_obj(self, student_uuid):
    #     return Teacher.objects.get(c_bh=student_uuid)

    def get_uuid(self):
        return str(uuid.uuid1()).replace('-', '')

    def get(self, request):
        body_data = request.data
        the_teacher = self.get_queryset().get(c_bh=body_data.get('c_bh'))
        the_obj = self.get_serializer(instance=the_teacher)
        return Response(the_obj.data, status=status.HTTP_200_OK)

    def post(self, request):
        body_data = request.data
        teacher_uuid = self.get_uuid()
        the_obj = self.get_serializer(data=body_data)
        the_obj.is_valid(raise_exception=True)
        the_obj.save(c_bh=teacher_uuid)
        return Response(the_obj.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        body_data = request.data
        the_teacher = self.get_queryset().get(c_bh=body_data.get('c_bh'))
        the_obj = self.get_serializer(instance=the_teacher, data=body_data)
        the_obj.is_valid(raise_exception=True)
        the_obj.save()
        return Response(the_obj.data, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
