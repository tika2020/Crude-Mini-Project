from django.shortcuts import render,redirect
from ecmsapp.models import Users
from django.http import JsonResponse

# Create your views here.
def Payment_Method(request):
    return render(request,'Enviroment/Payment_Method.html')
