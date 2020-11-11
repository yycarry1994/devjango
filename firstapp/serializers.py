from abc import ABC
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Kecheng, Student


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

    def validate_c_xueke(self, value):
        if not value.endwith('数学'):
            raise serializers.ValidationError('学科名称必须得以“数学”结尾')
        return value

    def create(self, validated_data):
        add_kecheng = Kecheng.objects.create(**validated_data)
        return add_kecheng

    def update(self, instance, validated_data):
        instance.c_xueke = validated_data.get('c_xueke')
        instance.save()
        return instance


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        # fields = '__all__'
        fields = ("c_name", "c_age", "c_sex")

    def create(self, validated_data):
        student = Student.objects.create(**validated_data)
        return student

    def update(self, instance, validated_data):
        student_obj = Student.objects.filter(c_bh=validated_data['c_bh']).update(**validated_data)
        return student_obj
