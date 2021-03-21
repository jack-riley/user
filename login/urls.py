from django.urls import path
from . import views

urlpatterns =[
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('wall', views.wall),
    path('error', views.error),
    path('process_message', views.process_message),
    path('process_comment', views.process_comment),
    path('logout', views.logout)


]