import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from django.utils.crypto import get_random_string

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






