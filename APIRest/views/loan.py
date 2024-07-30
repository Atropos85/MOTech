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
        #se obtiene la info del prestamo y se envia al serializer
        loan = get_loan(id)
        
        serializer = loan_Serializer (loan, many= True)       
        return Response(serializer.data)    

class CreateLoanView(APIView):    
    def post(self, request, format=None):
        #se obtiene el id del request
        customer_id = request.data.get('customer_id')
        
        #se obtiene la info del cliente
        try:
           customer = customers_customer.objects.get(id=customer_id)
        except customers_customer.DoesNotExist:
            raise NotFound(detail="Customer not found")
        #se obtiene el valor del score
        score= customer.score

        #Se calcula el total de la deuda
        total_debt = loans_loan.objects.filter(customer_id=customer_id).aggregate(
            total_debt=models.Sum('outstanding')
        )['total_debt'] or 0

        #Se obtiene el valor y el saldo del request
        amount = request.data.get('amount')
        outstanding = request.data.get('outstanding')

        #se valida que el valor y el saldo sean iguales
        if amount != outstanding:
            return Response(
                {"error": "The `amount` and `outstanding` fields must be equal."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        #Se valida que el cliente este activo
        if customer.status != 1:
            return Response(
                {"error": "The customer status must be active to create a loan."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        #se valida que el total de la deuda y el prestamo actual no supere el score del cliente
        if (total_debt + Decimal(amount)) > score:
            return Response(
                {"error": "The customer score is not enoght for the loan."},
                status=status.HTTP_400_BAD_REQUEST
            )

        #En caso de estar correcto se crea el prestamo
        serializer = loan_Serializer (data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)