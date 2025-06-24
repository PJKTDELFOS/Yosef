from django.shortcuts import render
from django.shortcuts import HttpResponse


# Create your views here.


def operacionalteste(request):
    return HttpResponse('estou no operacional')