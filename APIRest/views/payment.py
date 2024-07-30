
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.services import *
from ..serializer import *

# Create your views here.

class GetPaymentDetailView(APIView):
    def get(self, request, id):
        payments = get_payment(id)
        serializer = CusSerializer(payments)

        return Response(serializer.data)  

class CreatePaymentView(APIView):
    def post(self, request, format=None):
        customer_id = request.data.get('customer_id')
        external_id=request.data.get('external_id')
        amount = request.data.get('total_amount')
        total_amount=request.data.get('total_amount')

        create_payment(customer_id,external_id,amount,total_amount)
        
        return Response({
            'message': 'Payment processed successfully.',
        }, status=status.HTTP_201_CREATED)
        
class RejectedPaymentView(APIView):
    def post(self, request, format=None):
        payment_id = request.data.get('payment_id')

        rejected = rejected_payment(payment_id)

        return Response({
            'message': 'Payment rejected successfully.',
        }, status=status.HTTP_201_CREATED)
