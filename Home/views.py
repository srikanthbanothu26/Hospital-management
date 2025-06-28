from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *


def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)


def index(request):
    genders = Gender.objects.all()
    hospital = Hospital.objects.all()
    if request.user.is_authenticated:
        departments = Department.objects.all()
        doctors = Doctors.objects.all()

        if request.method == "POST":
            form = PatientForm(request.POST)
            if form.is_valid():
                form.save(user=request.user)
                return redirect('index')
        else:
            form = PatientForm()

        return render(request, 'index.html', {
            'departments': departments,
            'doctors': doctors,
            'genders': genders,
            'form': form,
            'hospital': hospital,
        })
    return render(request, 'usertype.html')


@superuser_required
def create_department(request):
    hospital = Hospital.objects.all()
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Or wherever you list departments
    else:
        form = DepartmentForm()
    return render(request, 'department_form.html', {'form': form, 'hospital': hospital})


@superuser_required
def update_department(request, department_id):
    hospital = Hospital.objects.all()
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'department_form.html', {'form': form, 'department': department, 'hospital': hospital})


@login_required
def create_doctor(request):
    hospital = Hospital.objects.all()
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  # Replace with your actual URL name
    else:
        form = DoctorForm()
    return render(request, 'doctors_form.html', {'form': form, 'hospital': hospital})


@superuser_required
def update_doctor(request, doctor_id):
    hospital = Hospital.objects.all()
    doctor = get_object_or_404(Doctors, id=doctor_id)
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('index')  # or any page
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctors_form.html', {'form': form, 'doctor': doctor, 'hospital': hospital})


@login_required
def medicines(request):
    hospital = Hospital.objects.all()
    products = Product.objects.all()
    return render(request, 'medicines_list.html', {'products': products, 'hospital': hospital})


@superuser_required
def create_medicine(request):
    hospital = Hospital.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicines')
    else:
        form = ProductForm()
    return render(request, 'medicine_form.html', {'form': form, 'hospital': hospital})


# Update
@superuser_required
def update_medicine(request, product_id):
    hospital = Hospital.objects.all()
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('medicines')
    else:
        form = ProductForm(instance=product)
    return render(request, 'medicine_form.html', {'form': form, 'product': product, 'hospital': hospital})


# Delete
@superuser_required
def delete_medicine(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('medicines')
