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
    path('app20201116/kechengs', views.GetKecheng.as_view(), name='get_kecheng'),
    path('app20201116/kechengs/<int:pk>', views.DealKecheng.as_view(), name='deal_kecheng'),
    path('app20201116/student', views.DealStudent.as_view(), name='deal_student'),
    path('app20201116/teacher', views.DealTeacher.as_view(), name='deal_teacher'),
    path('app20201116/students/<str:pk>', views.GetStudent.as_view(), name='get_student'),
    path('app20201116/homework1', views.HomeWork1.as_view(), name='HomeWork1'),
    path('app20201116/homework2', views.HomeWork2.as_view(), name='HomeWork2'),
]
