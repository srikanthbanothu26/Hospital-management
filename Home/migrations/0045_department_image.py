# Generated by Django 5.2.3 on 2025-07-02 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0044_usersinfo_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/images/services/'),
        ),
    ]
