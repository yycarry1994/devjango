"""firstproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('firstapp/index', views.index1, name='index'),
    path('firstapp/index2', views.index2.as_view(), name='index2'),
    path('firstapp/addstudent', views.AddStudent.as_view(), name='addstudent'),
    path('firstapp/addteacher', views.AddTeacher.as_view(), name='addteacher'),
    path('firstapp/addkecheng', views.AddKecheng.as_view(), name='addKecheng'),
    path('firstapp/addsource', views.AddSource.as_view(), name='addsource'),
    path('firstapp/kechengs', views.GetKecheng.as_view(), name='addkecheng'),
    path('firstapp/kechengs/<int:pk>', views.DealKecheng.as_view(), name='addkecheng2'),
]
