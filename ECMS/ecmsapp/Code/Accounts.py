import platform,socket
from user_agents import parse
from django.shortcuts import render,redirect
from ecmsapp.Code import *
from django.http import JsonResponse
from django.contrib.auth import authenticate, login,logout
from ecmsapp.models import userLoggers
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group, Permission

# Create your views here.

p = platform.uname()
host =socket.gethostname()
ipaddress = socket.gethostbyname(host)

@login_required(login_url='user_login')
def logout_view(request):
    if request.user.is_authenticated:
        user_agent_string = request.META.get('HTTP_USER_AGENT')
        user_agent = parse(user_agent_string)
        userinfo = f'{ipaddress} / {user_agent}'
        
        logout(request)
        messages.info(
                request, 'Logout!')
        msg = f"User Logged Out System"
        userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
        return redirect('user_login')


@login_required(login_url='user_login')
def staffs(request):
    users = User.objects.all()
    data = {
        'users': users
    }
    return render(request,'accounts/staffs.html',data)


@login_required(login_url='user_login')
def addUser(request):
    
    user_agent_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(user_agent_string)
    userinfo = f'{ipaddress} / {user_agent}'
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = '2023'
        status = False

        user =  User.objects.create_superuser(
            first_name=first_name, last_name=last_name,
            username=user_name, password=password,
            email=email, is_active=status
        )
        user.save()
        if user:
            # print(first_name,last_name,email,user_name)
            info = f'{first_name} {last_name} has been Successfuly Saved'
            msg = f"User Has Been Successfully Added {first_name} {last_name} to the System"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
            return JsonResponse({'success': True, 'message': info})
        else:
            msg = f"User Has Not Successfully Added {first_name} {last_name} to the System"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
            return JsonResponse({'success': False, 'message': 'Not Successfully added'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    

    
@login_required(login_url='user_login')
def activeAccount(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(user_agent_string)
    userinfo = f'{ipaddress} / {user_agent}'
    if request.method == 'POST':
        id = request.POST.get('id')
        password = request.POST.get('password')
        status = True

        user = User.objects.get(id=id)
        user.is_active = status
        user.set_password(password)
        user.save()
        if user:
            # print(first_name,last_name,email,user_name)
            info = f'{user.first_name} {user.last_name} has been Successfuly Activated'
            msg = f"User has been Successfuly Activated {user.first_name} {user.last_name} to the system"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()

            return JsonResponse({'success': True, 'message': info})
        else:
            msg = f"User has Not Successfuly Activated {user.first_name} {user.last_name} to the system"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
            return JsonResponse({'success': False, 'message': 'Not Successfully Activted'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    


@login_required(login_url='user_login')
def disableAccount(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(user_agent_string)
    userinfo = f'{ipaddress} / {user_agent}'
    if request.method == 'POST':
        id = request.POST.get('id')
        status = False

        user = User.objects.get(id=id)
        user.is_active = status
        user.save()
        if user:
            # print(first_name,last_name,email,user_name)
            info = f'{user.first_name} {user.last_name} has been Successfuly Disabled'
            msg = f"User has been Successfuly Disabled {user.first_name} {user.last_name} to the system"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
            return JsonResponse({'success': True, 'message': info})
        else:
            msg = f"User has Not Successfuly Disabled {user.first_name} {user.last_name} to the system"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
            return JsonResponse({'success': False, 'message': 'Not Successfully Disabled'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required(login_url='user_login')
def myprofile(request):
    
    return render (request, "accounts/myprofile.html")

@login_required(login_url='user_login')
def changepassword(request):
    
    user_agent_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(user_agent_string)
    userinfo = f'{ipaddress} / {user_agent}'
    
    if request.method == 'POST':
        id = request.POST.get('id')
        password = request.POST.get('password')
        

        userupdatePassword = User.objects.get(id=id)
        
        userupdatePassword.set_password(password)
        userupdatePassword.save()

        
        if userupdatePassword:
            info = f"{userupdatePassword.first_name} {userupdatePassword.last_name}'s Successfully Changed Password"
            response = {
                'success': True,
                'message': info
            }
            msg = f"User Has Been Successfully Changed {userupdatePassword.first_name} {userupdatePassword.last_name}'s Password"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
            return JsonResponse(response)
        else:
            messages.error(request,f"{userupdatePassword.username}'s Not Changed Password")
            msg = f"User Has Not Successfully Changed {userupdatePassword.first_name} {userupdatePassword.last_name}'s Password"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
            return redirect(myprofile)
    else:

        return redirect(myprofile)
