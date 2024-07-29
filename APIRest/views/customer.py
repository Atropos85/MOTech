from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from ..models import *
from ..serializer import *

# Create your views here.

class getcustomerView(APIView):
    def get(self, request, id):
        try:
           customer = customers_customer.objects.get(id=id)
        except customers_customer.DoesNotExist:
            raise NotFound(detail="Customer not found")
        
        serializer = customer_Serializer (customer)        
        return Response(serializer.data)   

class createcustomerView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = customer_Serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()  # Usa el método `create` personalizado del serializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerBalanceView(APIView):
    def get(self, request, id):
        try:
           customer = customers_customer.objects.get(id=id)
        except customers_customer.DoesNotExist:
           raise NotFound(detail="Customer not found")
         
        # Calcular total de la deuda
        total_debt = loans_loan.objects.filter(customer_id=id).aggregate(
            total_debt=models.Sum('outstanding')
        )['total_debt'] or 0
        
        # Obtener el score del cliente
        customer_id = customer.external_id
        score = customer.score
        
        # Calcular monto disponible
        available_amount = score - total_debt
        
        # Serializar la respuesta
        serializer = CustomerBalanceSerializer(data={
            'customer_id': customer_id,
            'score': score,
            'total_debt': total_debt,
            'available_amount': available_amount,
        })
        
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)