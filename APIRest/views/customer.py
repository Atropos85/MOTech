from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import csv
from io import StringIO
from ..models import *
from ..serializer import *

# Create your views here.

class listcustomerView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        customer = customers_customer.objects.all()
        serializer = customer_Serializer (customer, many=True)
        
        return Response(serializer.data)     

class getcustomerView(APIView):
    def get(self, request, id):
        customer = customers_customer.objects.get(id=id)
        serializer = customer_Serializer (customer)
        
        return Response(serializer.data)   
    
class createcustomerView(APIView):   
    def post(self, request, format=None, *args, **kwargs):
        serializer = customer_Serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerBalanceView(APIView):
    def get(self, request, id):
        customer = customers_customer.objects.get(id=id)
        
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