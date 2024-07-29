from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from ..models import *
from ..serializer import *

# Create your views here.

class getpaymentdetailView(APIView):
    def get(self, request, id):
        customer = customers_customer.objects.prefetch_related('payments').get(pk=id)
        serializer = CusSerializer(customer)

        return Response(serializer.data)  

class createpaymentView(APIView):
    def post(self, request, format=None):
        amount = float(request.data.get('total_amount'))
        customer_id = request.data.get('customer_id')
        customer = customers_customer.objects.get(id=customer_id)
        total_debt = loans_loan.objects.filter(customer_id=customer_id).aggregate(
            total_debt=models.Sum('outstanding')
        )['total_debt'] or 0
        
        if total_debt == 0:         
            new_status = 2     
            return Response({
                'message': 'There are no active loans with debt, payment rejected.',
            }, status=status.HTTP_201_CREATED)
        elif amount > total_debt:
            new_status = 2   
            return Response({
                'message': 'The payment amount exceeds the total debt, payment rejected.',
            }, status=status.HTTP_201_CREATED)
        else:
            new_status = 1

        payment = payments_payment(
            external_id=request.data.get('external_id'),
            total_amount=request.data.get('total_amount'),
            customer_id=customer,
            status=new_status  # Establecer el campo status basado en total_amount
        )        
        payment.save()
 
        if new_status == 2:
            return Response({
                'message': 'Payment Rejected.',
            }, status=status.HTTP_201_CREATED)
           
        remaining_amount = payment.total_amount

        loans = loans_loan.objects.filter(customer_id=customer_id, status=2)
        
        # Recorrer cada préstamo y actualizar el campo outstanding
        for loan in loans:
            if remaining_amount <= 0:
                break
                
            if loan.outstanding > remaining_amount:
                loan.outstanding -= remaining_amount
                
                payment_detail = payments_paymentdetail(
                    amount=remaining_amount,
                    payment_id=payment,
                    loan_id=loan
                )
                
                loan.save()
                payment_detail.save()
                
                remaining_amount = 0
            else:
                remaining_amount -= loan.outstanding
                amount = loan.outstanding 
                loan.outstanding = 0
                loan.status = 4  # Marca el préstamo como pagado
                
                payment_detail = payments_paymentdetail(
                    amount=amount,
                    payment_id=payment,
                    loan_id=loan
                )
                
                loan.save()
                payment_detail.save()

        return Response({
            'message': 'Payment processed successfully.',
        }, status=status.HTTP_201_CREATED)
        
class RejectedPaymentView(APIView):
    def post(self, request, format=None):
        payment_id = request.data.get('payment_id')

        paydetails = payments_paymentdetail.objects.filter(payment_id=payment_id)
    
        # Recorrer cada préstamo y actualizar el campo outstanding
        for paydetail in paydetails:
            payment = paydetail.payment_id
            loan = paydetail.loan_id
            amount = paydetail.amount

            payment.status = 2
            payment.save()

            loan.outstanding += amount
            loan.status = 2
            loan.save()

        return Response({
            'message': 'Payment rejected successfully.',
        }, status=status.HTTP_201_CREATED)
