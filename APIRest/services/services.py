from rest_framework.exceptions import NotFound, server_error
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from ..models import *

def get_customer(id):
    try:
        customer = customers_customer.objects.get(id=id)
    except customers_customer.DoesNotExist:
        raise NotFound(detail="Customer not found")

    return customer

def get_customer_balance(id):
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
        
        # Serializar la resp
        data={
            'customer_id': customer_id,
            'score': score,
            'total_debt': total_debt,
            'available_amount': available_amount,
        }

        return data

def get_loan(id):
    try:
        loan = loans_loan.objects.filter(customer_id=id)
    except loans_loan.DoesNotExist:
        raise NotFound(detail="Loan not found")
    
    return loan

def get_payment(id):
    try:
        customer = customers_customer.objects.prefetch_related('payments').get(pk=id)
    except loans_loan.DoesNotExist:
        raise NotFound(detail="Loan not found")
    
    return customer

def rejected_payment(id):

    paydetails = payments_paymentdetail.objects.filter(payment_id=id)

    # Recorrer cada préstamo y actualizar el campo outstanding
    for paydetail in paydetails:
        try:
            payment = paydetail.payment_id
            loan = paydetail.loan_id
            amount = paydetail.amount

            payment.status = 2
            payment.save()

            loan.outstanding += amount
            loan.status = 2
            loan.save()
        except loan.handler500:
            raise server_error(detail='Error proccesing Rejected Payment')
    
    
def create_payment(id,external_id,amount,total_amount):
        customer = customers_customer.objects.get(id=id)
        total_debt = loans_loan.objects.filter(customer_id=id).aggregate(
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
            customer_id=customer,
            external_id=external_id,
            total_amount=total_amount,            
            status=new_status  
        )        
        payment.save()
 
        if new_status == 2:
            return Response({
                'message': 'Payment Rejected.',
            }, status=status.HTTP_201_CREATED)
           
        remaining_amount = payment.total_amount

        loans = loans_loan.objects.filter(customer_id=id, status=2)
        
        # Recorrer cada préstamo y actualizar el campo outstanding
        for loan in loans:
            if remaining_amount <= 0:
                break
                
            if loan.outstanding > remaining_amount:
                loan.outstanding -= Decimal(remaining_amount)
                
                payment_detail = payments_paymentdetail(
                    amount=float(remaining_amount),
                    payment_id=payment,
                    loan_id=loan
                )
                
                loan.save()
                payment_detail.save()
                
                remaining_amount = 0
            else:
                remaining_amount -= Decimal(loan.outstanding)
                amount = loan.outstanding 
                loan.outstanding = 0
                loan.status = 4  # Marca el préstamo como pagado
                
                payment_detail = payments_paymentdetail(
                    amount=float(amount),
                    payment_id=payment,
                    loan_id=loan
                )
                
                loan.save()
                payment_detail.save()


    
        