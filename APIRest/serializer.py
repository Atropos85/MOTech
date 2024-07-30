from rest_framework import serializers
from .models import customers_customer, loans_loan, payments_payment, payments_paymentdetail

class customer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = customers_customer
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'status')

    def validate_score(self, value):
        """Valida que el score sea positivo."""
        if value <= 0:
            raise serializers.ValidationError("Score must be a positive number.")
        return value

    def validate_status(self, value):
        """Valida que el status sea un valor permitido."""
        if value not in dict(customers_customer.STATUS_CHOICES).keys():
            raise serializers.ValidationError(f"Status must be one of {dict(customers_customer.STATUS_CHOICES).values()}.")
        return value

    def create(self, validated_data):
        """Custom logic for creating a new Customer instance."""
        # Asignar un valor predeterminado para el campo status si no se proporciona
        validated_data.setdefault('status', customers_customer.STATUS_ACTIVE)

        # Crea y devuelve la instancia del modelo con los datos validados
        return customers_customer.objects.create(**validated_data)

class CustomerBalanceSerializer(serializers.Serializer):
    customer_id = serializers.CharField(max_length=40)
    score = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_debt = serializers.DecimalField(max_digits=12, decimal_places=2)
    available_amount = serializers.DecimalField(max_digits=12, decimal_places=2)

class loan_Serializer(serializers.ModelSerializer):
    class Meta:
        model = loans_loan
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'status')

    def __str__(self):
        return f"Loan {self.external_id} for Customer {self.customer_id}"

    def validate_amount(self, value):
        """Valida que el amount sea positivo."""
        if value <= 0:
            raise serializers.ValidationError("Amount must be a positive number.")
        return value

    def create(self, validated_data):
        """Custom logic for creating a new Loan instance."""
        # Asignar un valor predeterminado para el campo status si no se proporciona
        validated_data.setdefault('status', 2)

        # Crea y devuelve la instancia del modelo con los datos validados
        return loans_loan.objects.create(**validated_data)

class paymentdetail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = payments_paymentdetail
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'status', 'taken_at')

class payment_Serializer(serializers.ModelSerializer):
    payment_details = paymentdetail_Serializer(many=True, read_only=True)

    class Meta:
        model = payments_payment
        fields = '__all__'

class PayDetSerializer(serializers.ModelSerializer):
    loan_id = serializers.CharField(source = 'loan_id')
    payment_amount = serializers.DecimalField(source = 'amount',max_digits=20, decimal_places=10)
   
    class Meta:
        model = payments_paymentdetail
        fields = ['loan_id', 'amount']

class LoaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = loans_loan
        fields = ['external_id']

class PaySerializer(serializers.ModelSerializer):
    payment_details = PayDetSerializer(many=True, read_only=True)
    
    payment_external_id = serializers.CharField(source = 'external_id')
    total_amount = serializers.DecimalField(source = 'total_amount',max_digits=12, decimal_places=2)
    status = serializers.IntegerField(source = 'status')
    payment_date = serializers.DateTimeField(source = 'paid_at')
    
    class Meta:
        model = payments_payment
        fields = ['external_id', 'total_amount', 'status', 'paid_at', 'payment_details']

class CusSerializer(serializers.ModelSerializer):
    #loans = LoaSerializer(many=True, read_only=True)
    payments = PaySerializer(many=True, read_only=True)
    customer_external_id = serializers.IntegerField(source = 'external_id')
    class Meta:
        model = customers_customer
        fields = ['external_id', 'payments']
