from abc import ABC
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Kecheng


class KechengSerializer(serializers.Serializer):
    c_bh = serializers.IntegerField(label='c编号', help_text='c编号', read_only=True)
    c_xueke = serializers.CharField(label='学科',
                                    help_text='学科',
                                    validators=[UniqueValidator(Kecheng.objects.all(), message='学科名不能重复')],
                                    # write_only=True,
                                    max_length=5,
                                    min_length=2)
    create_time = serializers.DateTimeField(label='创建时间', help_text='创建时间', read_only=True)
    update_time = serializers.DateTimeField(label='更新时间', help_text='更新时间', read_only=True)


class KechengSerializer1(serializers.Serializer):
    c_xueke = serializers.CharField(label='学科', help_text='学科', max_length=5, min_length=2)