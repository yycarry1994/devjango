from rest_framework import serializers

class KechengSerializers(serializers.Serializer):
    c_xueke = serializers.CharField(label='学科')
    c_bh = serializers.ImageField(label='编号')
    c_createtime = serializers.DateField(label='创建时间')
    c_updatetime = serializers.DateField(label='更新时间')
