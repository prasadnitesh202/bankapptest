from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# define home function


def home(request):
    return HttpResponse('Hello World!')


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
<<<<<<< HEAD
    elif action=='expense-dateperiod':
        start_date=parameters.get('date-period').get('startDate')
        end_date=parameters.get('date-period').get('endDate')
        fulfillmentText={'fulfillmentText': 'You are looking for expenditure between'+str(start_date)+' and'+str(end_date)}
    elif action=='lastlogin':
        fulfillmentText={'fulfillmentText':'Last login details to be fetched from backend later'}
    elif action=='creditcardbill':
        fulfillmentText={'fulfillmentText':'Credit card bill for last month is:(to be fetched from db)'}



    
    # return response 
=======
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
    # return response
>>>>>>> 3d83dc82b0bd18bccf442bbaf06d19f2c5a1159a
    return JsonResponse(fulfillmentText, safe=False)