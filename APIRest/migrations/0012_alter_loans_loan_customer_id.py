# Generated by Django 5.0.7 on 2024-07-28 03:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIRest', '0011_alter_customers_customer_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loans_loan',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='APIRest.customers_customer'),
        ),
    ]