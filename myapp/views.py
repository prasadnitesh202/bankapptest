from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json

#demo account number for testing chatbot
acc_no=7673368716

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

        
    # return response
    return JsonResponse(fulfillmentText, safe=False)