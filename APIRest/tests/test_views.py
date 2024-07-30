from rest_framework.test import APITestCase
from rest_framework import status
from .test_models import customers_customer, loans_loan, payments_payment
from django.urls import reverse

class CustomerViewTests(APITestCase):
    def setUp(self):
        self.customer = customers_customer.objects.create(
            external_id="CUST123",
            score=1000.00
        )
        self.url_get_customer = reverse('APIRest:Get_Customer', args=[self.customer.id])
        self.url_create_customer = reverse('APIRest:Create_Customer')

    def test_get_customer(self):
        response = self.client.get(self.url_get_customer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'CUST123')

    def test_create_customer(self):
        data = {'external_id': 'CUST124', 'score': 1200.00}
        response = self.client.post(self.url_create_customer, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['external_id'], 'CUST124')

class LoanViewTests(APITestCase):
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
        self.url_get_loan = reverse('APIRest:Get_Loan', args=[self.customer.id])
        self.url_create_loan = reverse('APIRest:Create_Loan')

    def test_get_loan(self):
        response = self.client.get(self.url_get_loan)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'LOAN123')

    def test_create_loan(self):
        data = {'external_id': 'LOAN124', 'amount': 600.00, 'outstanding': 600.00, 'customer_id': self.customer.id}
        response = self.client.post(self.url_create_loan, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['external_id'], 'LOAN124')

class PaymentViewTests(APITestCase):
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
        self.payment = payments_payment.objects.create(
            external_id="PAY123",
            total_amount=200.00,
            customer_id=self.customer,
            status=1
        )
        self.url_get_payment_detail = reverse('APIRest:Get_PaymentDetail', args=[self.payment.id])
        self.url_create_payment = reverse('APIRest:Create_Payment')
        self.url_rejected_payment = reverse('APIRest:Rejected_Payment')

    def test_get_payment_detail(self):
        response = self.client.get(self.url_get_payment_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'PAY123')

    def test_create_payment(self):
        data = {'external_id': 'PAY124', 'total_amount': 300.00, 'status': 1, 'customer_id': self.customer.id}
        response = self.client.post(self.url_create_payment, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rejected_payment(self):
        response = self.client.post(self.url_rejected_payment, {'payment_id': self.payment.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
