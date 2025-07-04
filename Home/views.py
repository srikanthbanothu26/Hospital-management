from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
from django.http import JsonResponse


def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)


def index(request):
    genders = Gender.objects.all()
    hospital = Hospital.objects.all()
    if request.user.is_authenticated:
        departments = Department.objects.filter(image__isnull=False).exclude(image='')
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
    return render(request, 'usertype.html', {'hospital': hospital})


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
        form = DepartmentForm(request.POST, request.FILES, instance=department)
        if form.is_valid():
            form.save()
            return redirect('departments_list')
    else:
        form = DepartmentForm(instance=department)

    return render(request, 'department_form.html', {
        'form': form,
        'department': department,
        'hospital': hospital
    })


def departments_list(request):
    departments = Department.objects.all()
    hospital = Hospital.objects.all()
    return render(request, 'services.html', {'departments': departments, 'hospital': hospital})


def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    department.delete()
    return redirect('departments_list')


def bulk_delete_departments(request):
    ids = request.GET.get('ids', '')
    if ids:
        id_list = [int(id) for id in ids.split(',') if id.isdigit()]
        Department.objects.filter(id__in=id_list).delete()
    return redirect('departments_list')


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
            return redirect('specialists_list')  # or any page
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctors_form.html', {'form': form, 'doctor': doctor, 'hospital': hospital})


def specialists_list(request):
    doctors = Doctors.objects.all()
    hospital = Hospital.objects.all()
    return render(request, 'specialists.html', {'specialists': doctors, 'hospital': hospital})


def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctors, id=doctor_id)
    doctor.delete()
    return redirect('specialists_list')


def bulk_delete_doctors(request):
    ids = request.GET.get('ids', '')
    if ids:
        id_list = [int(id) for id in ids.split(',') if id.isdigit()]
        Doctors.objects.filter(id__in=id_list).delete()
    return redirect('specialists_list')


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


def get_states(request):
    country_id = request.GET.get('country_id')
    print("Requested Country ID:", country_id)

    states = States.objects.filter(country_id=country_id).values('id', 'name')
    return JsonResponse({'states': list(states)})


def user_info_view(request, user_id):
    hospital = Hospital.objects.all()
    if not request.user.is_authenticated:
        return redirect('login')

    # Allow access if admin OR the current user matches the user_id
    if not (request.user.is_superuser or request.user.id == int(user_id)):
        return HttpResponseForbidden("❌ You are not authorized to access this profile.")

    user_obj = get_object_or_404(User, id=user_id)
    user_info, created = UsersInfo.objects.get_or_create(name=user_obj)

    if request.method == 'POST':
        form = UsersInfoForm(request.POST, request.FILES, instance=user_info)
        state_id = request.POST.get('state')
        if form.is_valid():
            updated_user_info = form.save(commit=False)
            if state_id:
                updated_user_info.state_id = state_id
            updated_user_info.save()
            return redirect('index')  # stay on the same user's profile
    else:
        form = UsersInfoForm(instance=user_info)

    return render(request, 'user_info.html', {
        'form': form,
        'user_info': user_info,
        'viewing_user': user_obj,
        'hospital': hospital,  # to show "Profile of {{ viewing_user.username }}" in template
    })


def profession_list(request):
    professions = Profession.objects.all()
    hospital = Hospital.objects.all()
    return render(request, 'professions.html', {'professions': professions, 'hospital': hospital})


def profession_detail(request, profession_id):
    hospital = Hospital.objects.all()
    profession = get_object_or_404(Profession, id=profession_id)

    if request.method == 'POST':
        form = ProfessionForm(request.POST, instance=profession)
        if form.is_valid():
            form.save()
            return redirect('professions')
    else:
        form = ProfessionForm(instance=profession)

    return render(request, 'profession_detail.html', {
        'form': form,
        'profession': profession,
        'hospital': hospital
    })


def create_profession(request):
    hospital = Hospital.objects.all()

    if request.method == 'POST':
        form = ProfessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('professions')
    else:
        form = ProfessionForm()

    return render(request, 'profession_detail.html', {
        'form': form,
        'hospital': hospital
    })


def delete_profession(request, profession_id):
    profession = get_object_or_404(Profession, id=profession_id)
    profession.delete()
    messages.success(request, "Profession deleted successfully.")
    return redirect('professions')
