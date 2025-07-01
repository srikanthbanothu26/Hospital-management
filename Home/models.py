from dataclasses import fields

from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10)
    currency = models.CharField(max_length=10)
    currency_symbol = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name},{self.code}"


class Contact(models.Model):
    code = models.CharField(max_length=4, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Hospital(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    logo = models.ImageField(null=True, blank=True, upload_to="static/images/")
    country = models.ForeignKey('Country', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()

    def __str__(self):
        return self.name


class States(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    code = models.CharField(max_length=10, null=True, blank=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


from datetime import date


class Doctors(models.Model):
    profile_image = models.ImageField(upload_to="static/images/doctors/", default='static/images/logo.png')
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.ForeignKey('Gender', on_delete=models.CASCADE, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    specialization = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.FloatField(default=0.0)
    experience = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name.username} ({self.age} years old)"

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
                age -= 1
            return age
        return 'N/A'


class Profession(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Staff(models.Model):
    profile_image = models.ImageField(upload_to="static/images/staffs/", default='static/images/logo.png')
    name = models.CharField(max_length=100)
    profession = models.ForeignKey('Profession', on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    salary = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name} ({self.age} years old)"

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
                age -= 1
            return age
        return 'N/A'


class Patient(models.Model):
    reference = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=300)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.ForeignKey('Gender', on_delete=models.CASCADE, null=True, blank=True)
    datetime = models.DateTimeField()
    phone_number = models.CharField(max_length=300)
    address = models.TextField()
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.age} years old)"

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
                age -= 1
            return age
        return 'N/A'


class UsersInfo(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_image = models.ImageField(upload_to="static/images/user_profiles/", null=True, blank=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey('States', on_delete=models.CASCADE, null=True, blank=True)
    profession = models.ForeignKey('Profession', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name.username


class Chatter(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='chatters')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class Product(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Bill(models.Model):
    bill_status = [
        ('draft', 'Draft'),
        ('done', 'Done'),
    ]
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=bill_status, default='draft')
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Bill #{self.id} for {self.patient.name}"


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} in Bill #{self.bill.id}"


class DebitAccount(models.Model):
    debit_account_number = models.CharField(max_length=100)
    debit_ifsc_code = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.debit_account_number},{self.debit_ifsc_code}"


class CreditAccount(models.Model):
    credit_account_number = models.CharField(max_length=100)
    credit_ifsc_code = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.credit_account_number}, {self.credit_ifsc_code}"


class UpiPayments(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    payment_status = [
        ('not_paid', 'Not Paid'),
        ('paid', 'Paid'),
    ]
    ref = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    bill = models.ForeignKey('Bill', on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    credit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=payment_status, default='not_paid')
    debit_account = models.ForeignKey('DebitAccount', on_delete=models.CASCADE, null=True, blank=True)
    credit_account = models.ForeignKey('CreditAccount', on_delete=models.CASCADE, null=True, blank=True)
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.ref
