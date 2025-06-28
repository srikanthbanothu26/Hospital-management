from django.contrib import admin

from .models import Department, Doctors, Staff, Profession, Patient, Gender, Product, Bill, BillItem, Payment, \
    PaymentMethod, UpiPayments, DebitAccount, CreditAccount, Hospital, Contact
from .forms import DoctorsForm


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc')


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization')
    form = DoctorsForm


class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender')


class GenderAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Contact)
admin.site.register(Hospital)
admin.site.register(Gender, GenderAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Doctors, DoctorAdmin)
admin.site.register(Profession)
admin.site.register(Staff)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Product)
admin.site.register(Bill)
admin.site.register(BillItem)
admin.site.register(Payment)
admin.site.register(PaymentMethod)
admin.site.register(UpiPayments)
admin.site.register(DebitAccount)
admin.site.register(CreditAccount)
