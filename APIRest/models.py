from django.db import models
import uuid as uuid_id

# Create your models here.

class customers_customer(models.Model):
    #id = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length= 40, unique=True)
    status = models.PositiveSmallIntegerField(default = 1)
    score = models.DecimalField(max_digits=12, decimal_places=2)
    preapproved_at = models.DateTimeField()

class loans_loan(models.Model):
    #id = models.IntegerField
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length= 40, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.SmallIntegerField(default = 1)
    contract_version = models.CharField(max_length= 50,null=True)
    maximun_payment_date = models.DateTimeField(null=True)
    taken_at = models.DateTimeField(auto_now=True)
    customer_id = models.ForeignKey(customers_customer, on_delete=models.CASCADE)
    outstanding = models.DecimalField(max_digits=12, decimal_places=2)


class payments_payment(models.Model):
    #id = models.IntegerField
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    external_id = models.CharField(max_length= 40)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.SmallIntegerField()
    paid_at = models.DateTimeField()
    customer_id = models.IntegerField()

class payments_paymentdetail(models.Model):
    #id = models.IntegerField
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    loan_id = models.IntegerField()
    payment_id = models.IntegerField()
