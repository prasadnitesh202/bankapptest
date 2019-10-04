from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import formats
from .models import *
from .helperfunctions import *
import json
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .forms import BankUserForm
#demo account number for testing chatbot
acc_no=76733687163

# define home function
def home(request):
    return render(request,'myapp/Bank.html')

def login(request):
    return render(request,'myapp/Login.html')

def chatbot(request):
    return render(request,'myapp/Chatbot.html')





@csrf_exempt
def webhook(request):
    # build a request object
    req = json.loads(request.body)
    # get action from json
    action = req.get('queryResult').get('action')
    parameters = req.get('queryResult').get('parameters')
    # return a fulfillment message
    parameters = req.get('queryResult').get('parameters')
    if action == 'get_accnum':
        account_type = parameters.get('account-type')
        if account_type == 'Savings':
            fulfillmentText = {'fulfillmentText': 'Your savings account has \
            balanced toppings'}
        else:
            fulfillmentText = {'fulfillmentText': 'Speaking to you from \
            backend'}
    elif action == 'expense-dateperiod':
        start_date = parameters.get('date-period').get('startDate')
        end_date = parameters.get('date-period').get('endDate')
        fulfillmentText = {'fulfillmentText': 'You are looking for expenditure\
         between'+str(start_date)+' and'+str(end_date)}


    elif action == 'lastlogin':
        fulfillmentText = {'fulfillmentText': 'Last login details to be\
         fetched from backend later'}


    elif action == 'creditcardbill':
        fulfillmentText = {'fulfillmentText': 'Credit card bill for last month\
         is:(to be fetched from db)'}


    elif action =='emi_status':
        a=EMI.objects.filter(loan_id__acc_no=acc_no)
        text=""
        for i in a:
            text=text+' emi id: '+str(i.loan_id)+'\t'+'installment: '+str(i.installment)+'\n'
        if text=="":
            fulfillmentText={'fulfillmentText':'You dont have any emi in your account'}
        else: 
            fulfillmentText={'fulfillmentText':'Your EMI status is \n'+text}
    elif action=='fd-general':
        a=FixedDeposit.objects.filter(acc_no__acc_no=acc_no)
        c=a.count()
        text=""
        if c==0:
            text="You dont have any fixed deposit linked to your account "
        else:
            text="you have "+str(c)+" fixed deposits linked in your account"+' \n '
            c=0
            for i in a:
                text=text+'('+str(c+1)+') amount : '+str(i.amount)+'\t'+'startdate: '+str(i.start_date)+'\t'+' end date: '+str(i.end_date)+'\t'+' interest: '+str(i.interest)
                c=c+1
    
        fulfillmentText={'fulfillmentText':'Your Fixed deposit status is:: \n'+text}
    elif action=='fd-amount':
        a=FixedDeposit.objects.filter(acc_no__acc_no=acc_no)
        c=a.count()
        if(c==0):
            text="0. You dont have any fixed deposit linked to bank account"
        else:
            text="You have a total of "+str(c)+" fixed deposits linked to your bank account"
            c=0
            for i in a:
                text=text+'\n'+str(c+1)+': '+'  amount: '+str(i.amount)+'\n  '
                c=c+1
        fulfillmentText={'fulfillmentText':text}

    elif action=='fd-dateperiod':
        a=FixedDeposit.objects.filter(acc_no__acc_no=acc_no)
        c=a.count()
        print(c)
        if(c==0):
            text="You dont have any fixed deposit linked to bank account. Please get in touch with our customer care to know about fixed deposit schemes or you can ask me too"

        else:
            text="You have a total of "+str(c)+" fixed deposits linked to your bank account"
            c=0
            for i in a:
                text=text+'\n'+str(c+1)+':'+'  amount: '+str(i.amount)+' expires on  '+str(i.end_date)+'\n'
                c=c+1
        fulfillmentText={'fulfillmentText':text}

    elif action=='transaction-timeperiod':
        start_date = parameters.get('date-period').get('startDate')
        print(type(start_date))
        # s=dateutil.parser.parse('start_date')
        # print(s)
        d1 = datefield_parse(start_date)
        # d2 = datetime.datetime.strptime("2013-07-10T11:00:00.000Z","%Y-%m-%dT%H:%M:%S.%fZ")
        print(d1)


   
        end_date = parameters.get('date-period').get('endDate')
        d2=datefield_parse(end_date)
        print(d2)
        text='You have spend the following: '+'\n'
        a=Transaction.objects.filter(acc_no__acc_no=acc_no).filter(date_time__date__range=[d1, d2])
        for i in a:
            text=text+" amount: "+str(i.amount)+" on "+str(i.date_time)[0:19]+' and'

        fulfillmentText={'fulfillmentText':text}
        print(a)



            





        
    # return response
    return JsonResponse(fulfillmentText, safe=False)


def register(request):
    form = UserCreationForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})

def login_request(request):
    form_class = BankUserForm
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
        if BankUser.objects.filter(name=username).filter(password=password).count() == 1:
            print("Success")
        else:
            print("Failure")
    else:
        form = form_class()
    return render(request = request,
                    template_name = "myapp/Login.html",
                    context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")