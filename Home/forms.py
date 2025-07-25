from django import forms
from .models import Doctors, Patient, Gender, Department, Product, UsersInfo, Profession
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class DoctorsForm(forms.ModelForm):
    class Meta:
        model = Doctors
        fields = ['profile_image', 'name', 'specialization', 'date_of_birth', 'gender', 'salary']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].queryset = User.objects.filter(is_staff=True)


from datetime import datetime


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'date_of_birth', 'gender', 'phone_number', 'address', 'desc', 'datetime']

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)

        # Assign user
        if user:
            instance.user = user

        # Generate reference
        year = datetime.now().year
        prefix = f"PA/{year}/"
        last_patient = Patient.objects.filter(reference__startswith=prefix).order_by('-id').first()
        last_number = int(last_patient.reference.split("/")[-1]) if last_patient else 0
        instance.reference = f"{prefix}{str(last_number + 1).zfill(5)}"

        if commit:
            instance.save()
        return instance


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctors
        fields = ['profile_image', 'name', 'display_name', 'gender', 'date_of_birth', 'specialization', 'salary',
                  'experience', ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'desc', 'image']
        widgets = {
            'desc': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and not image.content_type in ['image/jpeg', 'image/png', 'image/webp']:
            raise ValidationError("Unsupported image format. Please upload JPEG, PNG, or WebP.")
        return image


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input w-full'}),
            'price': forms.NumberInput(attrs={'class': 'form-input w-full'}),
        }


class UsersInfoForm(forms.ModelForm):
    class Meta:
        model = UsersInfo
        fields = ['profile_image', 'country', 'city', 'profession']


class ProfessionForm(forms.ModelForm):
    class Meta:
        model = Profession
        fields = ['name', ]
