# Generated by Django 5.2.3 on 2025-06-28 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0034_alter_hospital_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
