# Generated by Django 5.0.7 on 2024-07-29 19:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIRest', '0017_alter_loans_loan_customer_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments_paymentdetail',
            name='loan_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_details', to='APIRest.loans_loan'),
        ),
        migrations.AlterField(
            model_name='payments_paymentdetail',
            name='payment_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_details', to='APIRest.payments_payment'),
        ),
    ]