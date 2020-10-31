from django.db import models


class BaseModel(models.Model):
    c_bh = models.AutoField(primary_key=True, verbose_name='主键', help_text='主键')
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='更新时间', auto_now=True)

    class Meta:
        # a.指定该模型类为抽象模型类，在迁移时不会创建该表
        # b.仅用于被其他类继承
        abstract = True
