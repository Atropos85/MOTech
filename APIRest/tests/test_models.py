from django.test import TestCase
from ..models import customers_customer, loans_loan, payments_payment, payments_paymentdetail
from django.core.exceptions import ValidationError

class CustomerModelTests(TestCase):
    def setUp(self):
        self.customer = customers_customer.objects.create(
            external_id="CUST123",
            score=1000.00
        )

    def test_customer_str(self):
        self.assertEqual(str(self.customer), "Customer CUST123")

    def test_customer_score_validation(self):
        with self.assertRaises(ValidationError):
            invalid_customer = customers_customer(
                external_id="CUST124",
                score=-100.00
            )
            invalid_customer.clean()

class LoanModelTests(TestCase):
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

    def test_loan_str(self):
        self.assertEqual(str(self.loan), "Loan LOAN123 for Customer CUST123")

    def test_loan_amount_validation(self):
        with self.assertRaises(ValidationError):
            invalid_loan = loans_loan(
                external_id="LOAN124",
                amount=-100.00,
                outstanding=-100.00,
                customer_id=self.customer
            )
            invalid_loan.clean()

class PaymentModelTests(TestCase):
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

    def test_payment_str(self):
        self.assertEqual(str(self.payment), "Payment PAY123 for Customer CUST123")

    def test_payment_status_paid(self):
        self.payment.status = 1
        self.payment.save()
        self.assertIsNotNone(self.payment.paid_at)

class PaymentDetailModelTests(TestCase):
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
        self.payment_detail = payments_paymentdetail.objects.create(
            amount=200.00,
            loan_id=self.loan,
            payment_id=self.payment
        )

    def test_payment_detail_str(self):
        self.assertEqual(str(self.payment_detail), "Detail for Payment PAY123")
