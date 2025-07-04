# Generated by Django 5.2.3 on 2025-06-27 20:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0020_alter_product_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debit_account_name', models.CharField(max_length=100)),
                ('debit_ifsc_code', models.CharField(max_length=100)),
                ('credit_account_name', models.CharField(max_length=100)),
                ('credit_ifsc_code', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UpiPayments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(blank=True, max_length=100, null=True)),
                ('debit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('credit', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.bill')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.patient')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.paymentmethod')),
            ],
        ),
    ]
