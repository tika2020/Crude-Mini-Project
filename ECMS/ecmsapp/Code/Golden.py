import platform
import socket

from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect, render
from user_agents import parse

from ecmsapp.models import Golden, userLoggers

# Create your views here.

p = platform.uname()
host =socket.gethostname()
ipaddress = socket.gethostbyname(host)


@login_required(login_url='user_login')
def golden(request):
    
    goldens = Golden.objects.filter(status=0)
    context = {'data': goldens}

        
    return render(request,'Enviroment/goldenhouse.html',context)


@login_required(login_url='user_login')
def createGoldenHouse(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(user_agent_string)
    userinfo = f'{ipaddress} / {user_agent}'

    if request.method == 'POST':
        new_district = request.POST['district']
        new_type = request.POST['type']
        new_houseno = request.POST['houseno']
        new_status = request.POST['status']

        if new_district != "" and new_type != "" and new_houseno != "" and new_status != "":
            add_house = Golden(district=new_district, type=new_type, houseno=new_houseno, status=new_status)
            add_house.save()
            isError = True
            msg = f"({new_district}-{new_type}-{new_houseno}) House Has Successfuly Added to the System"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
            return HttpResponse(isError)
        else:
            isError = False
            msg = f"({new_district}-{new_type}-{new_houseno}) House Not Successfuly Added to the System"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
            return HttpResponse(isError)


@login_required(login_url='user_login')
def update_GoldenHouse(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(user_agent_string)
    userinfo = f'{ipaddress} / {user_agent}'
    if request.method == 'POST':
        id = request.POST.get('id')
        district = request.POST.get('district')
        type = request.POST.get('type')
        houseno = request.POST.get('houseno')

        
        houseUpdate = Golden.objects.get(id=id)

        houseUpdate.district = district
        houseUpdate.type = type
        houseUpdate.houseno = houseno

        houseUpdate.save()
        if houseUpdate:
            msg = f"({district}-{type}-{houseno}) House Has Successfuly Updated to the System"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
        else:
            msg = f"({district}-{type}-{houseno}) House Not Successfuly Updated to the System"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()

        isError = False
        if isError:
            message = "Failure updating"
            return HttpResponse(message)
        else:
            message = "Successfully Update"
            return HttpResponse(message)
        



def delete_GoldenHouse(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(user_agent_string)
    userinfo = f'{ipaddress} / {user_agent}'
    if request.method == 'POST':
        id = request.POST.get('id')
        status = request.POST.get('status')

        
        houseUpdate = Golden.objects.get(id=id)

        houseUpdate.status = status

        houseUpdate.save()
        if houseUpdate:
            msg = f"({houseUpdate.district}-{houseUpdate.type}-{houseUpdate.houseno}) House Has Successfuly Deleted to the System"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
        else:
            msg = f"({houseUpdate.district}-{houseUpdate.type}-{houseUpdate.houseno}) House Not Successfuly Deleted to the System"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()

        isError = False
        if isError:
            message = "Failure Deleting"
            return HttpResponse(message)
        else:
            message = "Successfully Deleted"
            return HttpResponse(message)
    




def fetch_data(request):
    
    data = Golden.objects.filter(status=0)
    result=[]
    for row in data:
        result.append(row)
    print(result)
    return JsonResponse(result, safe=False)
