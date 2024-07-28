from rest_framework import serializers
from.models import customers_customer
from.models import loans_loan
from.models import payments_payment
from.models import payments_paymentdetail

class customer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = customers_customer
        fields = '__all__'

class CustomerBalanceSerializer(serializers.Serializer):
    customer_id = serializers.CharField(max_length= 40)
    score = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_debt = serializers.DecimalField(max_digits=12, decimal_places=2)
    available_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
       
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
        

class CustomePaymentsSerializer(serializers.Serializer):
    payment_external_id = serializers.CharField(max_length= 40)
    customer_external_id = serializers.CharField(max_length= 40)
    loan_external_id = serializers.CharField(max_length= 40)
    payment_date =  serializers.DateTimeField()
    status = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    payment_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
       