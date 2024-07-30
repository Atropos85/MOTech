from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.services import *
from ..serializer import *
from rest_framework.exceptions import NotFound
from decimal import Decimal
# Create your views here.
    
class GetLoanView(APIView):
    def get(self, request, id):
        
        loan = get_loan(id)
        
        serializer = loan_Serializer (loan, many= True)       
        return Response(serializer.data)    

class CreateLoanView(APIView):    
    def post(self, request, format=None):
        
        customer_id = request.data.get('customer_id')
        
        try:
           customer = customers_customer.objects.get(id=customer_id)
        except customers_customer.DoesNotExist:
            raise NotFound(detail="Customer not found")
    
        score= customer.score

        total_debt = loans_loan.objects.filter(customer_id=customer_id).aggregate(
            total_debt=models.Sum('outstanding')
        )['total_debt'] or 0
        amount = request.data.get('amount')
        outstanding = request.data.get('outstanding')

        if amount != outstanding:
            return Response(
                {"error": "The `amount` and `outstanding` fields must be equal."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if customer.status != 1:
            return Response(
                {"error": "The customer status must be active to create a loan."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if (total_debt + Decimal(amount)) > score:
            return Response(
                {"error": "The customer score is not enoght for the loan."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = loan_Serializer (data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)