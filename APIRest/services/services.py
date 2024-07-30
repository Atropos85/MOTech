from rest_framework.exceptions import NotFound, server_error
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from ..models import *

#Funcion para traer la informacion del cliente
def get_customer(id):
    try:
        customer = customers_customer.objects.get(id=id)
    except customers_customer.DoesNotExist:
        raise NotFound(detail="Customer not found")

    return customer

#Funcion para traer el balance del cliente
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
        
        # Creacion  del objeto data con la info para serializarla en la vista
        data={
            'customer_id': customer_id,
            'score': score,
            'total_debt': total_debt,
            'available_amount': available_amount,
        }

        return data

#Funcion para traer la informacion del prestamo
def get_loan(id):
    try:
        loan = loans_loan.objects.filter(customer_id=id)
    except loans_loan.DoesNotExist:
        raise NotFound(detail="Loan not found")
    
    return loan

#Funcion para traer la informacion deldetalle del prestamo
def get_payment(id):
    try:
        customer = customers_customer.objects.prefetch_related('payments').get(pk=id)
    except loans_loan.DoesNotExist:
        raise NotFound(detail="Loan not found")
    
    return customer

#Funcion para traer procesar el pago rechazado
def rejected_payment(id):

    #obtener el listado de los pagos(detalle)
    paydetails = payments_paymentdetail.objects.filter(payment_id=id)

    # Recorrer cada pago 
    for paydetail in paydetails:
        try:
            #Actualiza la informacion del pago
            payment = paydetail.payment_id
            loan = paydetail.loan_id
            amount = paydetail.amount

            payment.status = 2
            payment.save()

            #Actualiza la informacion del pppprestamo
            loan.outstanding += amount
            loan.status = 2
            loan.save()
        except loan.handler500:
            raise server_error(detail='Error proccesing Rejected Payment')
    
    
def create_payment(id,external_id,amount,total_amount):
          #Se obtiene la informacion del cliente
        customer = customers_customer.objects.get(id=id)
        # se calcula la deuda total
        total_debt = loans_loan.objects.filter(customer_id=id).aggregate(
            total_debt=models.Sum('outstanding')
        )['total_debt'] or 0
        
        #Valida que el cliente tenga prestamos activos
        if total_debt == 0:         
            new_status = 2     
            return Response({
                'message': 'There are no active loans with debt, payment rejected.',
            }, status=status.HTTP_201_CREATED)
        #valida que el valor del pago no supere el valor de la deuda
        elif amount > total_debt:
            new_status = 2   
            return Response({
                'message': 'The payment amount exceeds the total debt, payment rejected.',
            }, status=status.HTTP_201_CREATED)
        else:
            new_status = 1

        #crea el pago
        payment = payments_payment(
            customer_id=customer,
            external_id=external_id,
            total_amount=total_amount,            
            status=new_status  
        )        
        payment.save()
        
        #Envia mensaje que el pago fue rechazado pero se crea aun asi el pago
        if new_status == 2:
            return Response({
                'message': 'Payment Rejected.',
            }, status=status.HTTP_201_CREATED)

        #se setea el valor del pago en una variable para ir restandocelo para la distribucion de los pagos  
        remaining_amount = payment.total_amount

        #se obitiene el listado de prestamos activos
        loans = loans_loan.objects.filter(customer_id=id, status=2)
        
        # Recorrer cada préstamo y actualizar el campo outstanding
        for loan in loans:
            if remaining_amount <= 0:
                break
                
            #si el valor del saldo del prestamo es mayo al valor restante del pago 
            if loan.outstanding > remaining_amount:
                #resta el valor el saldo del prestamo
                loan.outstanding -= Decimal(remaining_amount)
                
                #Asigna los valores para el detalle del apgo
                payment_detail = payments_paymentdetail(
                    amount=float(remaining_amount),
                    payment_id=payment,
                    loan_id=loan
                )
                
                #salva el prestamo y el detalle del pago
                loan.save()
                payment_detail.save()
                
                #setea el valor del pago en 0
                remaining_amount = 0
            # Si el valor restante del pago es mayor al saldo del prestamo
            else: 
                #resta el valor del saldo del prestamo al valor remanente del apgo
                remaining_amount -= Decimal(loan.outstanding)
                "asigna los valores"
                amount = loan.outstanding 
                loan.outstanding = 0
                loan.status = 4  # Marca el préstamo como pagado
                
                #Crea el detalle del pago
                payment_detail = payments_paymentdetail(
                    amount=float(amount),
                    payment_id=payment,
                    loan_id=loan
                )
                
                loan.save()
                payment_detail.save()


    
        