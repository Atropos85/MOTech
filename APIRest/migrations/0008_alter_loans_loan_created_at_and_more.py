# Generated by Django 5.0.7 on 2024-07-27 02:49

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIRest', '0007_alter_loans_loan_external_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loans_loan',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='loans_loan',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='APIRest.customers_customer'),
        ),
        migrations.AlterField(
            model_name='loans_loan',
            name='external_id',
            field=models.UUIDField(blank=True, default=uuid.UUID('10694481-231e-45f6-899e-c1158aec0688'), null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='loans_loan',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]