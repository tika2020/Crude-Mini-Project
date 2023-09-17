import datetime,platform,socket
from user_agents import parse
from django.shortcuts import render,redirect
from ecmsapp.models import Service,Transaction,userLoggers
from datetime import date
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

p = platform.uname()
host =socket.gethostname()
ipaddress = socket.gethostbyname(host)


@login_required(login_url='user_login')
def transaction(request):
    serviceList = Service.objects.filter(status=0)
    alltransactions = Transaction.objects.filter(status=0)
    get_last_id = Transaction.objects.order_by('-id').first()
    current_year = datetime.datetime.now().year

    today = date.today()

    data = {
        'dataService': serviceList,
        'dataTransaction': alltransactions,
        'today': today,
        'currentYear': current_year,
        'getLastId': get_last_id
    }
    return render(request,'Enviroment/Transaction.html',data)

@login_required(login_url='user_login')
def makePayment(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(user_agent_string)
    userinfo = f'{ipaddress} / {user_agent}'

    if request.method == 'POST':
        pay_service = request.POST.get('service')
        accounts = request.POST.get('account')
        pay_date = request.POST.get('date')
        pay_price = 5
        pay_status = 0

        info = ""

        servid = Service.objects.get(id=pay_service)

        info += f"Renter : {servid.enviroment.renter.name}-{servid.enviroment.renter.tell}\n"
        info += f"House : {servid.enviroment.house.district}-{servid.enviroment.house.houseno}-({servid.enviroment.house.type})\n"
        info += f"Account : {accounts}\n"
        info += f"date : {pay_date} and Price {pay_price}\n"

        # print(info)
        addrow = Transaction(service=servid,date=pay_date,status=pay_status,account=accounts,price=pay_price)
        addrow.save()
        if addrow:
            servid.process = "Paid"
            servid.save()
            response = {
                'success': True,
                'message': f'Your transaction has been created by {info}',
                'error': f'Not Saved by {info}'
            }
            
            
            msg = f"{servid.enviroment.renter.name} Was Been Successfuly Maked Payment with {servid.enviroment.house.district}-{servid.enviroment.house.houseno}-({servid.enviroment.house.type}) and Added to the System"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
            
            
            return JsonResponse(response)
            
        else:
            response = {
                'error': True,
                'message': f'Not Saved by {info}'
            }
            msg = f"{servid.enviroment.renter.name} Was Not Successfuly Maked Payment with {servid.enviroment.house.district}-{servid.enviroment.house.houseno}-({servid.enviroment.house.type}) and Added to the System"
            userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()
            return JsonResponse(response)


def generateInvoice(request):
    
    user_agent_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(user_agent_string)
    userinfo = f'{ipaddress} / {user_agent}'

    if request.method == "POST":
        renter = request.POST.get("name")
        ref = request.POST.get("refno")
        today = request.POST.get("today")

        msg = f"Reference No {ref} Has Been Genereated By {renter} as invoice and Added to the System"
        userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()





        # print(f"{renter} {ref} {today}")

        response = {
            'success': True,
            'message': 'Successfully generated'

        }
        return JsonResponse(response)
    else:
        redirect(transaction)

def printInvoice(request):
    
    user_agent_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(user_agent_string)
    userinfo = f'{ipaddress} / {user_agent}'

    if request.method == "POST":
        ref = request.POST.get("ref")

        msg = f"Reference No {ref} Has Been Printed"
        userLoggers(logger_name=request.user,device=userinfo,message=msg,level="INFO").save()


        print(f" {ref} ")

        response = {
            'success': True,
            'message': 'Successfully generated'

        }
        return JsonResponse(response)
    else:
        redirect(transaction)



