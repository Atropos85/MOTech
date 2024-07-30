
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.services import *
from ..serializer import *
from decimal import Decimal

# Create your views here.

class GetPaymentDetailView(APIView):
    def get(self, request, id):
        #se obtiene la info del pago y se envia al serializer
        payments = get_payment(id)
        serializer = CusSerializer(payments)

        return Response(serializer.data)  

class CreatePaymentView(APIView):
    def post(self, request, format=None):
        customer_id = request.data.get('customer_id')
        external_id=request.data.get('external_id')
        amount = request.data.get('total_amount')
        total_amount=request.data.get('total_amount')
        #se toman los datos del request y se envia a la funcion
        create_payment(customer_id,external_id,amount,total_amount)
        
        return Response({
            'message': 'Payment processed successfully.',
        }, status=status.HTTP_201_CREATED)
        
class RejectedPaymentView(APIView):
    def post(self, request, format=None):
        #se obtiene el id del pago de request
        payment_id = request.data.get('payment_id')
        #se se ejecuta la funcion 
        rejected = rejected_payment(payment_id)

        return Response({
            'message': 'Payment rejected successfully.',
        }, status=status.HTTP_201_CREATED)
