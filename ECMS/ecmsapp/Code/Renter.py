import platform,socket
from user_agents import parse
from django.shortcuts import render,redirect,HttpResponse
from ecmsapp.models import Renter,userLoggers
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

p = platform.uname()
host =socket.gethostname()
ipaddress = socket.gethostbyname(host)

@login_required(login_url='user_login')
def renter(request):
       
    renters = Renter.objects.filter(status=0)
    context = {'data':renters}
    return render(request,'Enviroment/renter.html',context)


@login_required(login_url='user_login')
def createRenter(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(user_agent_string)
    userinfo = f'{ipaddress} / {user_agent}'
    if request.method == 'POST':
        new_name = request.POST['name']
        new_tell = request.POST['tell']
        new_martial_status = request.POST['martial_status']
        new_status = request.POST['status']

        if new_name != "" and new_tell != "" and new_martial_status != "" and new_status != "":
            add_renter = Renter(name=new_name, tell=new_tell, martial_status=new_martial_status, status=new_status)
            add_renter.save()
            msg = f"({new_name}-{new_tell}-{new_martial_status}) Renter Has Successfuly Added to the System"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
            isError = True
            return HttpResponse(isError)
        else:
            
            msg = f"({new_name}-{new_tell}-{new_martial_status}) Renter Not Successfuly Added to the System"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
            isError = False
            return HttpResponse(isError)
        

@login_required(login_url='user_login')
def update_renter(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(user_agent_string)
    userinfo = f'{ipaddress} / {user_agent}'
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        tell = request.POST.get('tell')
        martial_status = request.POST.get('martial_status')

        
        renterUpdate = Renter.objects.get(id=id)
        
        # print(f"{id} {name} {tell} {martial_status}")
        renterUpdate.name = name
        renterUpdate.tell = tell
        renterUpdate.martial_status = martial_status

        renterUpdate.save()

        if renterUpdate:
            
            msg = f"({renterUpdate.name}-{renterUpdate.tell}-{renterUpdate.martial_status}) Renter Has Successfuly Updated to the System"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()

        else:
            msg = f"({renterUpdate.name}-{renterUpdate.tell}-{renterUpdate.martial_status}) Renter Not Successfuly Updated to the System"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
            

        isError = False
        if isError:
            message = "Failure updating"
            return HttpResponse(message)
        else:
            message = "Successfully Update"
            return HttpResponse(message)
        
    

@login_required(login_url='user_login')
def delete_renter(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(user_agent_string)
    userinfo = f'{ipaddress} / {user_agent}'
    if request.method == 'POST':
        id = request.POST.get('id')
        status = request.POST.get('status')

        # print(f"{id} {status}")

        
        renterUpdate = Renter.objects.get(id=id)

        renterUpdate.status = status

        renterUpdate.save()

        if renterUpdate:
            
            msg = f"({renterUpdate.name}-{renterUpdate.tell}-{renterUpdate.martial_status}) Renter Has Successfuly Deleted to the System"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
        else:
            msg = f"({renterUpdate.name}-{renterUpdate.tell}-{renterUpdate.martial_status}) Renter Not Successfuly Deleted to the System"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()


        isError = False
        if isError:
            message = "Failure Deleting"
            return HttpResponse(message)
        else:
            message = "Successfully Deleted"
            return HttpResponse(message)
    

