# Generated by Django 5.2.3 on 2025-06-20 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0007_alter_staff_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctors',
            name='salary',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='staff',
            name='salary',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='staff',
            name='profile_image',
            field=models.ImageField(default='static/images/logo.png', upload_to='static/images/staffs/'),
        ),
    ]
