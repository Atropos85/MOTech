from rest_framework.test import APITestCase
from rest_framework import status
from .test_models import customers_customer, loans_loan, payments_payment
from .test_serializers import customer_Serializer, loan_Serializer, payment_Serializer

class CustomerSerializerTests(APITestCase):
    def setUp(self):
        self.customer = customers_customer.objects.create(
            external_id="CUST123",
            score=1000.00
        )
        self.valid_data = {
            'external_id': 'CUST124',
            'score': 1200.00
        }
        self.invalid_data = {
            'external_id': 'CUST125',
            'score': -50.00
        }

    def test_valid_serializer(self):
        serializer = customer_Serializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['score'], 1200.00)

    def test_invalid_serializer(self):
        serializer = customer_Serializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('score', serializer.errors)

class LoanSerializerTests(APITestCase):
    def setUp(self):
        self.customer = customers_customer.objects.create(
            external_id="CUST123",
            score=1000.00
        )
        self.loan = loans_loan.objects.create(
            external_id="LOAN123",
            amount=500.00,
            outstanding=500.00,
            customer_id=self.customer
        )
        self.valid_data = {
            'external_id': 'LOAN124',
            'amount': 600.00,
            'outstanding': 600.00,
            'customer_id': self.customer.id
        }
        self.invalid_data = {
            'external_id': 'LOAN125',
            'amount': -100.00,
            'outstanding': -100.00,
            'customer_id': self.customer.id
        }

    def test_valid_serializer(self):
        serializer = loan_Serializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['amount'], 600.00)

    def test_invalid_serializer(self):
        serializer = loan_Serializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('amount', serializer.errors)

class PaymentSerializerTests(APITestCase):
    def setUp(self):
        self.customer = customers_customer.objects.create(
            external_id="CUST123",
            score=1000.00
        )
        self.payment = payments_payment.objects.create(
            external_id="PAY123",
            total_amount=200.00,
            customer_id=self.customer,
            status=1
        )
        self.valid_data = {
            'external_id': 'PAY124',
            'total_amount': 300.00,
            'status': 1,
            'customer_id': self.customer.id
        }
        self.invalid_data = {
            'external_id': 'PAY125',
            'total_amount': -100.00,
            'status': 1,
            'customer_id': self.customer.id
        }

    def test_valid_serializer(self):
        serializer = payment_Serializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['total_amount'], 300.00)

    def test_invalid_serializer(self):
        serializer = payment_Serializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('total_amount', serializer.errors)
