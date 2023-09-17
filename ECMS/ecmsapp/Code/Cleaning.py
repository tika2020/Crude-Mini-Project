import platform,socket
from user_agents import parse
from django.shortcuts import render,redirect,HttpResponse
from ecmsapp.models import Service,Enviroment,House,userLoggers
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
p = platform.uname()
host =socket.gethostname()
ipaddress = socket.gethostbyname(host)



@login_required(login_url='user_login')
def cleaning(request):

    user_agent_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(user_agent_string)
    userinfo = f'{ipaddress} / {user_agent}'


    district =House.objects.values('district').distinct()
    
    enviroments = Enviroment.objects.filter(status=0)
    cleaning = Service.objects.filter(status=0)
    context = {
        'enviroData':enviroments,
        'serviceData':cleaning,
        'district':district
    }

    if request.method == 'POST':
        new_enviroments = request.POST['enviroment']
        new_date = request.POST['date']
        new_status = request.POST['status']

        envid = Enviroment.objects.get(id=new_enviroments)

        if new_enviroments != "" and new_date != "" and new_status != "":
            add_services = Service(date=new_date,status=new_status,enviroment_id=envid.id)
            add_services.save()
            if add_services.pk:            
                msg = f"{envid.house.district} District - {envid.house.type} Type House No-{envid.house.houseno} Was Successfuly Cleaned and Added to the System"
                userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
            else:
                msg = f"{envid.house.district} District - {envid.house.type} Type House No-{envid.house.houseno} Was Not Successfuly Cleaned and Added to the System"
                userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()

    return render(request,'Enviroment/cleaning.html',context)


