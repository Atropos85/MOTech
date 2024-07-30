from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.services import *
from ..serializer import *

# Create your views here.

class GetCustomerView(APIView):
    def get(self, request, id):
        #se obtiene la info del customer y se envia al serializer
        customer = get_customer(id)
        serializer = customer_Serializer (customer)        
        return Response(serializer.data)   

class CreateCustomerView(APIView):
    def post(self, request, *args, **kwargs):
        #Serializa el request
        serializer = customer_Serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()  # Usa el método `create` personalizado del serializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerBalanceView(APIView):
    #se obtiene el balance del customer y se envia al serializer
    def get(self, request, id):
        serializar_data = get_customer_balance(id)
        serializer = CustomerBalanceSerializer(serializar_data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)