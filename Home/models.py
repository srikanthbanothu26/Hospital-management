from django.db import models
from django.contrib.auth.models import User


class Gender(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()

    def __str__(self):
        return self.name


from datetime import date


class Doctors(models.Model):
    profile_image = models.ImageField(upload_to="static/images/doctors/", default='static/images/logo.png')
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.ForeignKey('Gender', on_delete=models.CASCADE, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    specialization = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.FloatField(default=0.0)

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
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)
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
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    tota_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def total_amount(self):
        self.tota_amount = sum(item.product.price for item in self.items.all())
        return sum(item.product.price for item in self.items.all())

    def __str__(self):
        return f"Bill #{self.id} for {self.patient.name}"


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} in Bill #{self.bill.id}"
