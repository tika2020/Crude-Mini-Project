import platform,socket
from user_agents import parse
from django.shortcuts import render,redirect,HttpResponse
from ecmsapp.models import House,userLoggers
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

p = platform.uname()
host =socket.gethostname()
ipaddress = socket.gethostbyname(host)


@login_required(login_url='user_login')
def house(request):
    
    houses = House.objects.filter(status=0) 
    context = {'data': houses}

        
    return render(request,'Enviroment/house.html',context)


@login_required(login_url='user_login')
def createHouse(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(user_agent_string)
    userinfo = f'{ipaddress} / {user_agent}'
    if request.method == 'POST':
        new_district = request.POST['district']
        new_type = request.POST['type']
        new_houseno = request.POST['houseno']
        new_status = request.POST['status']

        if new_district != "" and new_type != "" and new_houseno != "" and new_status != "":
            add_house = House(district=new_district, type=new_type, houseno=new_houseno, status=new_status)
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
def update_house(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(user_agent_string)
    userinfo = f'{ipaddress} / {user_agent}'
    if request.method == 'POST':
        id = request.POST.get('id')
        district = request.POST.get('district')
        type = request.POST.get('type')
        houseno = request.POST.get('houseno')

        
        houseUpdate = House.objects.get(id=id)

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
        



def delete_house(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(user_agent_string)
    userinfo = f'{ipaddress} / {user_agent}'
    if request.method == 'POST':
        id = request.POST.get('id')
        status = request.POST.get('status')

        
        houseUpdate = House.objects.get(id=id)

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
    
    data = House.objects.filter(status=0)
    result=[]
    for row in data:
        result.append(row)
    print(result)
    return JsonResponse(result, safe=False)
