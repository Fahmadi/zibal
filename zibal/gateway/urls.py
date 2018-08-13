from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.createUser, name='createUser'),
    path('welcome', views.welcomeUser, name='welcomeUser'),
    path('creategateway', views.creategateway, name='creategateway'),
]
