from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from Home.models import *


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('user_login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def login(request):
    role = request.GET.get('role')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User not found. Please check your credentials or sign up to login.")
            return render(request, 'login.html', {'role': role})

        # User exists; now check password
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if role == 'admin':
                if user.is_superuser:
                    auth_login(request, user)
                    return redirect('index')
                else:
                    messages.error(request, "Not authorized as admin.")
            elif role == 'user':
                if user.is_staff and Doctors.objects.filter(name=user).exists():
                    auth_login(request, user)
                    return redirect('index')
                elif not user.is_staff and not user.is_superuser:
                    auth_login(request, user)
                    return redirect('index')
                else:
                    messages.error(request, "Unauthorized user.")
            else:
                messages.error(request, "Invalid role specified.")
        else:
            messages.error(request, "Password incorrect. Please check again or reset your password.")

    return render(request, 'login.html', {'role': role})


def logout(request):
    auth_logout(request)
    return redirect('index')


def update_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        try:
            user = User.objects.get(username=username)  # Assign user properly

            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, 'update_password.html')

            user.set_password(password)  # Use Django's secure password setter
            user.save()
            messages.success(request, "Password updated successfully.")
            return redirect('index')

        except User.DoesNotExist:
            messages.error(request, "User not found. Please check your credentials or sign up to login.")
            return render(request, 'update_password.html')

    return render(request, 'update_password.html')
