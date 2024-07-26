from rest_framework import viewsets
from APIRest import models
from APIRest import serializer

# Create your views here.

class customerViewSet(viewsets.ModelViewSet):
    queryset = models.customers_customer.objects.all() 
    serializer_class = serializer.customer_Serializer 
    
class loanViewSet(viewsets.ModelViewSet):
    queryset = models.loans_loan.objects.all() 
    serializer_class = serializer.loan_Serializer
    
class paymentViewSet(viewsets.ModelViewSet):
    queryset = models.payments_payment.objects.all() 
    serializer_class = serializer.payment_Serializer 
    
class paymentdetailViewSet(viewsets.ModelViewSet):
    queryset = models.payments_paymentdetail.objects.all() 
    serializer_class = serializer.paymentdetail_Serializer 
    