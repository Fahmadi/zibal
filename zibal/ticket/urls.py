from django.urls import path

from . import views

urlpatterns = [
    path('new', views.createTicket, name='createTicket'),

]