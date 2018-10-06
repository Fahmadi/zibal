import json
from datetime import datetime

import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse , JsonResponse
from django.template.loader import get_template
from django.utils.crypto import get_random_string

from .mongoModel import Transaction
from .mongoModel import GatewayMerchant
from .models import User
from .utils import *
from oauth2_provider.decorators import protected_resource
import time

def payRequest(request):
    amount = request.json['amount']
    callback_url = request.json['callback_url']
    validmerch = GatewayMerchant.objects(merchant_key = request.json['merchant_key'])
    if (validmerch.count() > 0):
        merchant_key = request.json['merchant_key']
        pay_ir_api_key = 'test'
        mobile = '09101111111'
        zibalId = time.time()
        ross = Transaction(amount=amount, callback_url=callback_url, merchant_key=merchant_key , payir_transaction_id = pay_ir_api_key , status = False, zibalId=zibalId , mobile = mobile).save()
        return JsonResponse({"result":100, "url":"http://localhost:8000/gateway/start/"+str(int(zibalId))})
    else:
        return JsonResponse({"result":400})


def start(request, id):
    trans = Transaction.objects.get(zibalId=id)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    resp = requests.post('https://pay.ir/payment/send', json={'api': trans.payir_transaction_id , 'amount': trans.amount, 'redirect': 'http://127.0.0.1:8000/gateway/verifyPay', 'mobile': trans.mobile}, headers=headers).json()
    if(resp['status']==1):
        trans.transId = resp['transId']
        trans.save()
        return redirect('https://pay.ir/payment/gateway/'+str(trans.transId))



def verifyPay(request):
    if ( int(request.POST.get('status',default=0))== 1):
        # verify
        resp = requests.post('https://pay.ir/payment/verify',json={'api': 'test', 'transId': request.POST.get('transId')}).json()
        if(resp['status']==1):
            trans = Transaction.objects.get(transId= request.POST.get('transId'))
            trans.status = True
            trans.save()
            return render(request, 'zibal.html', {'callback_url': trans.callback_url,'status' : request.POST.get('status') , 'transId': request.POST.get('transId') } )
        else:
            return render(request, 'errorMessage.html', {'errorMessage': resp['errorMessage'],'errorCode': resp['errorCode']} )
    else:

        transac = Transaction.objects.get(transId = request.POST.get('transId'))
        return render(request, 'zibalnew.html', {'callback_url': transac.callback_url, 'status': request.POST.get('status'),
                                              'zibalId': transac.zibalId , 'message' : request.POST.get('message') })


def verifyCallback(request):
    # trans = Transaction.objects.get(transId=request.POST.get('transId'), merchant_key=request.POST.get('merchant_key'))
    trans = Transaction.objects(transId=request.json['transId'])
    if ( trans.count() > 0 ):
        if(trans[0].status==False):
            result = 0
            message = "پرداخت با موفقیت انجام نشد. "
        if(trans[0].status==True):
            result = 100
            message = "ok"
    else:
        result = -1
        message = "چنین پرداختی از سایت شما انجام نشده است."
    return JsonResponse({"result":result , "message":message})

# def usergatewayList(request):,
#     user_id = request.user.id
#     user_gateways = GatewayMerchant.objects.get(user_id)
#     for gateway in user_gateways:
#         print(user_gateways.title)