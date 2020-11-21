from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from firstapp.models import Kecheng, Student, Teacher, Source


class Homework1(serializers.Serializer):
    username = serializers.CharField(max_length=10, min_length=5, label='用户名', help_text='用户名')
    gender = serializers.ChoiceField(((1, '男'), (2, '女')), initial=2, label='性别', help_text='性别')

class HomeWork2(serializers.Serializer):
    item = serializers.CharField(min_length=2)
    score = serializers.IntegerField(min_value=0, max_value=100, write_only=True)

class Homeworks(serializers.Serializer):
    username = serializers.CharField(max_length=10, min_length=5, label='用户名', help_text='用户名')
    gender = serializers.ChoiceField(((1, '男'), (2, '女')), initial=2, label='性别', help_text='性别')
    hobbys = HomeWork2(label='项目信息', help_text='项目信息', many=True)


def is_container_project_word(value):
    if '老师' not in value:
        raise serializers.ValidationError('项目名称中必须得包含“项目”')


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
    source_kecheng_bh = serializers.StringRelatedField(read_only=True, many=True)  # 从表__str__返回的字段
    teacher_kecheng_cbh = serializers.StringRelatedField(read_only=True, many=True)

    def validate_c_xueke(self, value):
        if not value.endswith('数学'):
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

    # source = serializers.PrimaryKeyRelatedField(read_only=True, many=True)   #主表关联从表字段一定要加上many=True(主外键关联)
    source_student_bh = serializers.StringRelatedField(read_only=True, many=True)  #从表__str__返回的字段
    # source = serializers.SlugRelatedField(slug_field='c_fenshu', many=True, read_only=True)   #在从表中选择字段关联

    class Meta:
        model = Student
        fields = '__all__'
        # fields = ("c_name", "c_age", "c_sex", "source")

    def create(self, validated_data):
        student = Student.objects.create(**validated_data)
        return student

    def update(self, instance, validated_data):
        student_obj = Student.objects.filter(c_bh=validated_data['c_bh']).update(**validated_data)
        return student_obj


class TeacherSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(write_only=True)
    # kecheng = serializers.PrimaryKeyRelatedField(queryset=Kecheng.objects.all()  #使用的关联字段，附表的主键
    # kecheng = serializers.StringRelatedField(label='父表__str__所返回的字段', help_text='父表__str__所返回的字段') #__str__返回的字段
    c_x_bh = serializers.SlugRelatedField(slug_field='c_xueke', queryset=Kecheng.objects.all())  #可以选择自己想要关联的字段

    class Meta:
        model = Teacher
        fields = '__all__'
        # fields = ("c_name", "n_age", "c_sex", "c_bh", 'c_x_bh', 'kecheng', 'email')
        # a.可以指定不需要自动生成的模型类字段
        # exclude = ("c_bh", "c_x_bh")

        extra_kwargs = {
            'c_name': {
                'min_length': 2,
                'max_length': 5,
                'read_only': True,
                'validators': [
                    UniqueValidator(Teacher.objects.all(), message='教师名不能重复')
                ],
                'error_messages': {
                    'min_length': '教师名不能少于两位',
                    'max_length': '教师名不能少于五位',
                    'required': '教师名为必传参数'
                }
            },
            'c_bh': {
                'read_only': True
            },
            'c_sex': {
                'read_only': True
            },
            'c_x_bh': {
                'read_only': True
            }

        }

    def validate(self, attrs):
        teacher_name = attrs.get('c_name')
        teacher_age = attrs.get('n_age')
        if '老师' not in teacher_name or teacher_age <= 18:
            raise serializers.ValidationError('teacher名字必须包含“老师”并且年龄必须大于18')
        return attrs

    def create(self, validated_data):
        validated_data.pop('email')
        return super().create(validated_data)


class SourceSerializer(serializers.ModelSerializer):

    class Meta:
        module = Source
        filed = '__all__'

        extra_kwargs = {
            'c_x_bh': {

            }
        }


