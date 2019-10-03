from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json

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




            





        
    # return response
    return JsonResponse(fulfillmentText, safe=False)