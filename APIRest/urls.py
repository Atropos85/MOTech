from django.urls import path, include
from rest_framework import routers
from .views.customer import *
from .views.loan import *
from .views.payment import *

app_name = 'APIRest'
urlpatterns = [
    path(r'getcustomer/<id>/', GetCustomerView.as_view(), name='Get_Customer'), 
    path(r'createcustomer',CreateCustomerView.as_view(), name='Create_Customer'), 
    path(r'customerBalance/<id>/', CustomerBalanceView.as_view(), name='BalanceByCustomer'), 
    path(r'getloan/<id>/', GetLoanView.as_view(), name='Get_Loan'), 
    path(r'createloan', CreateLoanView.as_view(), name='Create_Loan'), 
    path(r'getpaymentdetail/<id>/', GetPaymentDetailView.as_view(), name='Get_PaymentDetail'), 
    path(r'createpayment', CreatePaymentView.as_view(), name='Create_Payment'),
    path(r'RejectedPayment', RejectedPaymentView.as_view(), name='Rejected_Payment'), 
]
    
