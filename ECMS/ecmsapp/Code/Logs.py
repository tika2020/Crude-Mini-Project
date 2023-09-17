from django.shortcuts import render,redirect
from ecmsapp.models import Service,Enviroment,userLoggers
from django.http import JsonResponse

# Create your views here.



def AuditLogs(request):
    logs = userLoggers.objects.all().order_by('-id')
    data = {
        'auditLogs': logs
    }
    return render(request,'Enviroment/auditLogs.html',data)



def Reports2(request):
    return render(request,'Enviroment/Reports2.html')
