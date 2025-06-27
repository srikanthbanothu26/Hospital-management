from django.shortcuts import render, redirect

from .models import *
from .forms import *


def index(request):
    genders = Gender.objects.all()
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
            'form': form
        })
    return render(request, 'usertype.html')



