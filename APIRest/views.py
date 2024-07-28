from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import *
from .serializer import *
from datetime import timezone
# Create your views here.

# class customerViewSet(viewsets.ModelViewSet):
#     queryset = models.customers_customer.objects.all() 
#     serializer_class = serializer.customer_Serializer 
    
class customerView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        customer = customers_customer.objects.all()
        serializer = customer_Serializer (customer, many=True)
        
        return Response(serializer.data)    
    
    def post(self, request, format=None):
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
      
class loanView(APIView):
    def get(self, request, id, format=None, *args, **kwargs):
        loan = loans_loan.objects.filter(customer_id=id)
        if loan:
           serializer = loan_Serializer (loan, many=True)       
           return Response(serializer.data)    
    
    def post(self, request, id, format=None):
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
    
class custpaymentView(generics.ListAPIView):

    queryset = customers_customer.objects.prefetch_related('loans_set').all()
    serializer_class = CustomerLoanSerializer
    
class paymentView(APIView):
    def get(self, request, id, format=None, *args, **kwargs):
        payment = payments_payment.objects.filter(customer_id=id)
        if payment:
           serializer = payment_Serializer (payment, many=True)       
           return Response(serializer.data)   
           
    def post(self, request, id,format=None):
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
                        sld_debt = 0
                        amount = loans.outstanding
                        
                        #loans.updated_at = timezone.now
                        loans.outstanding -= payment.total_amount
                        loans.save()
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
               
