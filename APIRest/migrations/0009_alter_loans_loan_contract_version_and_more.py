# Generated by Django 5.0.7 on 2024-07-27 03:50

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIRest', '0008_alter_loans_loan_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loans_loan',
            name='contract_version',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='loans_loan',
            name='external_id',
            field=models.UUIDField(blank=True, default=uuid.UUID('a6d4bcf5-e20a-4d92-b60a-c1b652d2b619'), null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='loans_loan',
            name='maximun_payment_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='loans_loan',
            name='taken_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
