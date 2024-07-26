from rest_framework import serializers
from.models import customers_customer
from.models import loans_loan
from.models import payments_payment
from.models import payments_paymentdetail

class customer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = customers_customer
        fields = '__all__'
        
class loan_Serializer(serializers.ModelSerializer):
    class Meta:
        model = loans_loan
        fields = '__all__'

class payment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = payments_payment
        fields = '__all__'

class paymentdetail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = payments_paymentdetail
        fields = '__all__'
        