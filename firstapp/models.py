from django.db import models
from utils.base_model import BaseModel

# Create your models here.


class Teacher(BaseModel):
    """
    教师表
    """
    c_bh = models.CharField(max_length=32, verbose_name='教师编号', help_text='c_bh', primary_key=True)
    c_name = models.CharField(max_length=32, verbose_name='老师姓名', help_text='老师姓名')
    c_x_bh = models.ForeignKey('Kecheng', on_delete=models.SET_NULL, null=True, related_name='teacher_kecheng_cbh')
    n_age = models.IntegerField(verbose_name='年龄', help_text='年龄')
    c_sex = models.CharField(max_length=2, verbose_name='性别', help_text='性别')

    def __str__(self):
        return self.c_name


class Student(BaseModel):
    """
    学生表
    """
    c_bh = models.CharField(max_length=32, verbose_name='学生编号', help_text='c_bh', primary_key=True)
    c_name = models.CharField(max_length=16, verbose_name='学生姓名', help_text='学生姓名')
    c_age = models.IntegerField(verbose_name='年龄', help_text='年龄')
    c_sex = models.CharField(max_length=2, verbose_name='性别', help_text='性别')

    def __str__(self):
        return self.c_name


class Kecheng(BaseModel):
    """
    课程表
    """
    c_xueke = models.CharField(max_length=32, verbose_name='学科', help_text='学科')


class Source(BaseModel):
    """
    成绩表
    """
    c_fenshu = models.IntegerField(verbose_name="分数", help_text="分数")

    c_x_bh = models.ForeignKey('Kecheng', on_delete=models.CASCADE, verbose_name='课程编号', help_text='课程编号',
                               related_name='source_kecheng_bh')
    c_s_bh = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True, verbose_name='学生编号', help_text='学生编号',
                               related_name='source_student_bh')

    def __str__(self):
        return str(self.c_fenshu)

