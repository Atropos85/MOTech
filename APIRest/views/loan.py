from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from ..models import *
from ..serializer import *
from datetime import timezone
# Create your views here.
    
class getloanView(APIView):
    def get(self, request, id):
        loan = loans_loan.objects.filter(customer_id=id)
        if loan:
           serializer = loan_Serializer (loan, many= True)       
           return Response(serializer.data)    

class createloanView(APIView):    
    def post(self, request, format=None):
        customer_id = request.data.get('customer_id')
        customer = customers_customer.objects.get(id=customer_id)
        score= customer.score

        total_debt = loans_loan.objects.filter(customer_id=customer_id).aggregate(
            total_debt=models.Sum('outstanding')
        )['total_debt'] or 0
        amount = request.data.get('amount')

        if customer.status != 1:
            return Response(
                {"error": "The customer status must be active to create a loan."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if (total_debt + amount) > score:
            return Response(
                {"error": "The customer score is not enoght for the loan."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = loan_Serializer (data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)