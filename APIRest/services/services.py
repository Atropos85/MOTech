from rest_framework.exceptions import NotFound
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
        