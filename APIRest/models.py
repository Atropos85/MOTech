from django.db import models

# Create your models here.

class customers_customer(models.model):
    id = models.IntegerField
    created_at = models.DateTimeField
    updated_at = models.DateTimeField
    external_id = models.CharField(max_length= 50)
    status = models.SmallIntegerField
    score = models.DecimalField(max_digits=12, decimal_places=2)
    preapproved_at = models.IntegerField

class loans_loan(models.model):
    id = models.IntegerField
    created_at = models.DateTimeField
    updated_at = models.DateTimeField
    external_id = models.CharField(max_length= 50)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.SmallIntegerField
    contract_version = models.CharField(max_length= 50)
    maximun_payment_date = models.DateTimeField
    taken_at = models.DateTimeField
    custoimer_id = models.IntegerField
    outstanding = models.DecimalField(max_digits=12, decimal_places=2)


class payments_payment(models.model):
    id = models.IntegerField
    created_at = models.DateTimeField
    updated_at = models.DateTimeField
    external_id = models.CharField(max_length= 50)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.SmallIntegerField
    paid_at = models.DateTimeField
    customer_id = models.IntegerField

class payments_paymentdetail(models.model):
    id = models.IntegerField
    created_at = models.DateTimeField
    updated_at = models.DateTimeField
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    loan_id = models.IntegerField
    payment_id = models.IntegerField