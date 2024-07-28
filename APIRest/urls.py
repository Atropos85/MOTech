from django.urls import path, include
from rest_framework import routers
from .views.customer import *
from .views.loan import *
from .views.payment import *

app_name = 'APIRest'
urlpatterns = [
    path(r'listcustomer', listcustomerView.as_view()), 
    path(r'getcustomer/<id>/', getcustomerView.as_view()), 
    path(r'createcustomer', createcustomerView.as_view()), 
    path(r'customerBalance/<id>/', CustomerBalanceView.as_view()), 
    path(r'getloan/<id>/', getloanView.as_view()), 
    path(r'createloan', createloanView.as_view()), 
    path(r'getpayment/<id>/', getpaymentView.as_view()), 
    path(r'getpaymentdetail/<id>/', getpaymentdetailView.as_view()), 
    path(r'createpayment', createpaymentView.as_view()),     
    path(r'customerpayments', customerpaymentdetailView.as_view()), 
    path(r'RejectedPayment', RejectedPaymentView.as_view()), 


    

]
    
