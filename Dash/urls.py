"""
URL configuration for Diary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from .views import *
from Dash.firebase import views as firebase_views


urlpatterns = [
      # Serve login or dashboard page
    path('', login_, name="login"),
    path("save_fcm_token/", firebase_views.save_fcm_token, name="save_fcm_token"),
    path('login', login_, name="login"),
  	path('logcode',logcode,name ="logcode"),
  	path('index',index,name="index"),
  	path('track',track,name="track"),
  	path('contact',contact,name="contact"),
  	path('help',help_,name="help"),
  	path('budget',budget,name="budget"),
  	path('invest',invest,name="invest"),
  	path('sponser',sponser,name="sponser"),

    path('add/<str:ID>/<str:AMOUNT>/<str:STATUS>/<str:REF>/', add_record, name='add_record'),

    path('delete/<str:record_id>/', delete_record_view, name='delete_record'),
    path("planner",planner,name = "planner"),



    path("add_task",add_task,name='add_task'),
    path("toggle_task",toggle_task,name='toggle_task'),
    path("delete_task/<int:task_id>/",delete_task,name='delete_task'),


    path("re_load",re_load,name="re_load"),
    
    path("add_budget",add_budget,name = "add_budget")
]	
