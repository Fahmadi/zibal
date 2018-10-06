import json
from datetime import datetime

import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.utils.crypto import get_random_string

from .mongoModel import Transaction
from .mongoModel import GatewayMerchant
from .models import User
from .utils import *
from oauth2_provider.decorators import protected_resource
import time

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

def validate_image(image):
    file_size = image.size
    limit_kb = 1150 * 1024
    if file_size > limit_kb:
        return False
    else:
        return True


def validate_file_extension(value):
    if value.content_type != 'application/jpg':
        return False
    else:
        return True

@login_required()
def uploadImage(request):
    user = User.objects.get(id = request.user.id)
    user.user_pic = request.FILES['user_pic']
    if validate_image(request.FILES['user_pic']) == False :
        return JsonResponse({"satus": False, })
    else:
        if validate_file_extension(request.FILES['user_pic']) == False :
            return JsonResponse({"satus": False})
        else:
            user.save()
            return JsonResponse({"status": True})

@login_required()
def creategateway(request):
    title = request.json['title']
    website = request.json['website']
    merchant_key = get_random_string(length=32)
    user_id = request.user.id
    ross = GatewayMerchant(title=title, website=website, merchant_key=merchant_key , user_id = user_id , user_activate = True).save()
    return JsonResponse({"merchant_key":merchant_key})