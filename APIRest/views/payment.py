from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from ..models import *
from ..serializer import *
from datetime import timezone
# Create your views here.

class getpaymentView(APIView):
    def  get(self, request, id):
        payment = payments_payment.objects.filter(customer_id=id)
        if payment:
           serializer = payment_Serializer (payment, many=True)       
           return Response(serializer.data)  

class getpaymentdetailView(APIView):
    def  get(self, request, id):
        payment = payments_paymentdetail.objects.filter(payment_id=id)
        if payment:
           serializer = paymentdetail_Serializer (payment, many=True)       
           return Response(serializer.data)   

class createpaymentView(APIView):           
    def post(self, request, format=None):
        amount = request.data.get('total_amount')
        customer_id = request.data.get('customer_id')
        customer = customers_customer.objects.get(id=customer_id)
        total_debt = loans_loan.objects.filter(customer_id=customer_id).aggregate(
            total_debt=models.Sum('outstanding')
        )['total_debt'] or 0
        
        if (total_debt) == 0:         
            new_status = 2     

            return Response({
                'message': 'There are not loans active with debt, payment rejected.',
            }, status=status.HTTP_201_CREATED)
        elif total_debt < amount:
            new_status = 2   
            
            return Response({
                'message': 'The value of the payment it is mayor of the total debt, payment rejected.',
            }, status=status.HTTP_201_CREATED)

        else:
            new_status = 1

        payment = payments_payment(
            external_id  = request.data.get('external_id'),
            total_amount = request.data.get('total_amount'),
            customer_id  = customer,
            status       = new_status  # Establecer el campo status basado en total_amount
        )        
        payment.save()
 
        if new_status == 1:
            sld_debt = payment.total_amount

            loan = loans_loan.objects.filter(customer_id=customer_id, status=2)
        
            # Recorrer cada préstamo y actualizar el campo outstanding
            for loans in loan:
                if sld_debt > 0:
                    if loans.outstanding > sld_debt:
                        
                        #loans.updated_at = timezone.now
                        loans.outstanding -= sld_debt
                        loans.save()

                        amount = sld_debt
                        sld_debt = 0

                        payments_detail = payments_paymentdetail(
                            amount=  amount,
                            payment_id = payment,
                            loan_id  = loans
                        )        
                        payments_detail.save()
                    else:
                        sld_debt -= loans.outstanding
                        amount = loans.outstanding
                        loans.outstanding = 0
                        #loan.updated_at = timezone.now
                        loans.status = 4
                        loans.save()
                        
                        payments_detail = payments_paymentdetail(
                            amount=  amount,
                            payment_id = payment,
                            loan_id  = loans
                        )        
                        payments_detail.save()


            return Response({
                'message': 'Payment processed successfully.',
                #'payment': serializer.data
            }, status=status.HTTP_201_CREATED)
               

class customerpaymentdetailView(generics.ListAPIView):

    queryset = customers_customer.objects.prefetch_related('loans_set').all()
    serializer_class = CustomerLoanSerializer
    