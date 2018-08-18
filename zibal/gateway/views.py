import json
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse , JsonResponse
from django.utils.crypto import get_random_string

from .mongoModel import Transaction
from .mongoModel import GatewayMerchant
from .models import User
from .utils import *
from oauth2_provider.decorators import protected_resource

def index(request):
    return JsonResponse(request.json)

def createUser(request):
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
        phone = request.json['phone']

        try:
            lenghtpass= LenghtPasswordValidator()
            lenghtpass.validate(password)

            alphapass=AlphaPasswordValidator()
            alphapass.validate(password)


            specialpass = SpecialCharactersPasswordValidator()
            specialpass.validate(password)



            user = User.objects.create_user(username=username, email=email
                                            , password=password,
                                            phone=phone)
            user.save()
            return JsonResponse({"status": True})
        except ValidationError as e:
            # lenghtpass.get_help_text()
            return JsonResponse({"message":e.message})

@login_required()
def welcomeUser(request):
    user = request.user
    return HttpResponse('Hello,'+ user.username)



def creategateway(request):
    title = request.json['title']
    website = request.json['website']
    merchant_key = get_random_string(length=32)
    user_id = request.user.id

    ross = GatewayMerchant(title=title, website=website, merchant_key=merchant_key , user_id = user_id , user_activate = True).save()
    return JsonResponse({"merchant_key":merchant_key})

def payRequest(request):
    amount = request.json['amount']
    callback_url = request.json['callback_url']
    merchant_key = request.json['merchant_key']
    pay_ir_api_key = 'test'
    mobile = '09101111111'
    ross = Transaction(amount=amount, callback_url=callback_url, merchant_key=merchant_key , payir_transaction_id = pay_ir_api_key , status = False).save()

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    resp = requests.post('https://pay.ir/payment/send', json={'api': pay_ir_api_key, 'amount': amount, 'redirect': 'http://127.0.0.1:8000/gateway/verifyPay', 'mobile': mobile}, headers=headers).json()
    ross.transId = resp['transId']
    ross.save()
    return JsonResponse({"url":"https://pay.ir/payment/gateway/"+str(resp['transId'])})

def verifyPay(request):
    if ( int(request.POST.get('status',default=0))== 1):

        trans = Transaction.objects.get(transId= request.POST.get('transId'))
        trans.status = True
        trans.save()
        # verify
        resp = requests.post('https://pay.ir/payment/verify',json={'api': 'test', 'transId': request.POST.get('transId')}).json()

        return render(request, 'zibal.html', {'callback_url': trans.callback_url,'status' : request.POST.get('status') , 'transId': request.POST.get('transId') } )


# def usergatewayList(request):,
#     user_id = request.user.id
#     user_gateways = GatewayMerchant.objects.get(user_id)
#     for gateway in user_gateways:
#         print(user_gateways.title)