# Generated by Django 5.2.3 on 2025-06-29 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0036_rename_tota_amount_bill_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('currency', models.CharField(max_length=10, unique=True)),
                ('currency_symbol', models.CharField(max_length=10, unique=True)),
            ],
        ),
    ]
