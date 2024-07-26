from django.contrib import admin
from.models import customers_customer
from.models import loans_loan
from.models import payments_payment
from.models import payments_paymentdetail

admin.site.register(customers_customer)
admin.site.register(loans_loan)
admin.site.register(payments_payment)
admin.site.register(payments_paymentdetail)
# Register your models here.
