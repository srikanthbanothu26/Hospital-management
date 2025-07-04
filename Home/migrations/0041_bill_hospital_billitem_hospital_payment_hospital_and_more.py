# Generated by Django 5.2.3 on 2025-06-30 08:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0040_hospital_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='hospital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Home.hospital'),
        ),
        migrations.AddField(
            model_name='billitem',
            name='hospital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Home.hospital'),
        ),
        migrations.AddField(
            model_name='payment',
            name='hospital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Home.hospital'),
        ),
        migrations.AddField(
            model_name='upipayments',
            name='hospital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Home.hospital'),
        ),
    ]
