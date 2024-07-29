from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class customers_customer(models.Model):
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 2
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_INACTIVE, 'Inactive'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=40, unique=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    score = models.DecimalField(max_digits=12, decimal_places=2)
    preapproved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['created_at']

    def __str__(self):
        return f"Customer {self.external_id}"

    def clean(self):
        """Validaciones personalizadas del modelo."""
        super().clean()
        if self.score <= 0:
            raise ValidationError({'score': 'Score must be a positive number.'})

    def save(self, *args, **kwargs):
        self.clean()  # Asegúrate de que las validaciones personalizadas se ejecuten al guardar
        super().save(*args, **kwargs)


class loans_loan(models.Model):
    # Opciones de estado para el préstamo
    LOAN_STATUS_CHOICES = [
        (1, 'Pending'),
        (2, 'Active'),
        (3, 'Rejected'),
        (4, 'Paid'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=40, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    outstanding = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.SmallIntegerField(choices=LOAN_STATUS_CHOICES, default=2)  # Estado por defecto 'Activo'
    contract_version = models.CharField(max_length=60, null=True, blank=True)
    maximun_payment_date = models.DateTimeField(null=True, blank=True)
    taken_at = models.DateTimeField(auto_now=True)  # Actualización automática de la fecha
    customer_id = models.ForeignKey(customers_customer, on_delete=models.CASCADE, related_name='loans')

    def clean(self):
        if self.amount <= 0:
            raise ValidationError({'amount': 'Amount must be a positive number.'})

    def save(self, *args, **kwargs):
        self.clean()  # Asegúrate de que las validaciones personalizadas se ejecuten al guardar
        super().save(*args, **kwargs)


class payments_payment(models.Model):
    STATUS_CHOICES = [
        (1, 'Completed'),  # Completado
        (2, 'Rejected'),   # Rechazado
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=40, unique=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, null=True)
    paid_at = models.DateTimeField(null=True, blank=True)  # Allow null and blank if payment is not completed yet
    customer_id = models.ForeignKey(customers_customer, on_delete=models.CASCADE, related_name='payments')

    def save(self, *args, **kwargs):
        # Update paid_at if status is Completed
        if self.status == 1 and not self.paid_at:
            self.paid_at = timezone.now()
        elif self.status == 2:
            self.paid_at = None  # Ensure paid_at is null if status is Rejected
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment {self.external_id} for Customer {self.customer_id.external_id}"


class payments_paymentdetail(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    loan_id = models.ForeignKey(loans_loan, on_delete=models.CASCADE, related_name='payment_details')
    payment_id = models.ForeignKey(payments_payment, on_delete=models.CASCADE, related_name='payment_details')

    def clean(self):
        # Ensure that amount is positive
        if self.amount <= 0:
            raise ValidationError('Amount must be positive.')
        
        # Ensure that amount does not exceed the total amount of the payment
        if self.payment_id:
            total_amount = self.payment_id.total_amount
            if self.amount > total_amount:
                raise ValidationError('Amount cannot be greater than the total amount of the payment.')

    def __str__(self):
        return f"Detail for Payment {self.payment_id.external_id}"
