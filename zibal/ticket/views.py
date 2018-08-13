from django.http import JsonResponse
from django.shortcuts import render

from .enums import ticket
from .models import Ticket
import datetime

def createTicket(request):
    subject = request.json['subject']
    department = request.json['department']
    text = request.json['text']

    in_reply_to = request.json.get('in_reply_to', None)
    date = datetime.datetime.now()
    if (in_reply_to != None):
        in_reply_to = Ticket.objects.get(id = in_reply_to)

    Ticket.objects.create(subject = subject, department = department, text = text , in_reply_to = in_reply_to, date= date , status=ticket.status_open)

    return JsonResponse({"status": True})

