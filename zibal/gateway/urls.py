from django.urls import path, re_path

from . import WebServiceViews, APIviews

urlpatterns = [
    path('', APIviews.index, name='index'),
    path('register', APIviews.createUser, name='createUser'),
    path('welcome', APIviews.welcomeUser, name='welcomeUser'),
    path('uploadImage', APIviews.uploadImage, name='uploadImage'),
    path('creategateway', APIviews.creategateway, name='creategateway'),
    path('payRequest', WebServiceViews.payRequest, name='payRequest'),
    path('verifyPay', WebServiceViews.verifyPay, name='verifyPay'),
    path('verify', WebServiceViews.verifyCallback, name='verifyCallback'),
    re_path('start/(?P<id>[0-9]+)/$', WebServiceViews.start, name='start'),
]