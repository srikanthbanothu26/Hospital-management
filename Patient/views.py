from django.shortcuts import render, redirect, get_object_or_404
from Home.models import *
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from Home.forms import *
from django.db.models import Q
from django.utils import timezone
from django.db.models import Sum


def patients(request):
    hospital = Hospital.objects.all()
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if user.is_superuser:
            patients = Patient.objects.all()
        else:
            patients = Patient.objects.filter(user=request.user)

        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        name_query = request.GET.get('name')

        if from_date:
            patients = patients.filter(datetime__date__gte=from_date)
        if to_date:
            patients = patients.filter(datetime__date__lte=to_date)
        if name_query:
            patients = patients.filter(
                Q(name__icontains=name_query) | Q(reference__icontains=name_query)
            )

        patients = patients.order_by('-datetime')

        return render(request, 'patients.html', {
            'patients': patients,
            'hospital': hospital,
            'latest_appointment': patients.first() if patients.exists() else None,
        })


def create_patient(request):
    genders = Gender.objects.all()
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('patients')
    else:
        form = PatientForm()
    return render(request, 'create_patient.html', {"form": form, "genders": genders})


def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    genders = Gender.objects.all()

    if request.method == "POST":
        patient.name = request.POST.get('name')
        patient.date_of_birth = request.POST.get('date_of_birth') or None
        gender_id = request.POST.get('gender')
        patient.gender = Gender.objects.get(id=gender_id) if gender_id else None
        patient.phone_number = request.POST.get('phone_number')
        patient.address = request.POST.get('address')
        patient.desc = request.POST.get('desc')
        patient.datetime = request.POST.get('datetime')
        patient.save()
        return redirect('patients')

    return render(request, 'edit_patient.html', {'patient': patient, 'genders': genders})


def bulk_delete_patients(request):
    ids = request.GET.get('ids')
    if ids:
        id_list = ids.split(',')
        Patient.objects.filter(id__in=id_list).delete()
        messages.success(request, "Selected patients deleted successfully.")
        return redirect('patients')
    else:
        messages.error(request, "No patients selected.")
    return redirect('patients')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def patient_pdf_view(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    return render_to_pdf('patient_report.html', {'patient': patient})


def patient_pdf_download(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    template = get_template('patient_report.html')
    html = template.render({'patient': patient})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Patient_{patient_id}.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response


def Bills(request):
    hospital = Hospital.objects.all()
    bills = Bill.objects.all().order_by('-date')
    total_sum = bills.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'bills.html', {'bills': bills, 'hospital': hospital, 'total_sum': total_sum})


def delete_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    bill.delete()
    return redirect('bills')


def bulk_delete_bills(request):
    ids = request.GET.get('ids', '')
    if ids:
        id_list = [int(id) for id in ids.split(',') if id.isdigit()]
        Bill.objects.filter(id__in=id_list).delete()
    return redirect('bills')


def create_bill(request):
    hospital = Hospital.objects.all()
    products = Product.objects.all()
    patient = None
    searched = False

    # Handle form submission
    if request.method == "POST":
        # 1. If search submitted
        if 'search_submit' in request.POST:
            search_term = request.POST.get("search_patient", "").strip()
            searched = True
            if search_term:
                patient = Patient.objects.filter(reference__iexact=search_term).first()
                if not patient:
                    patient = Patient.objects.filter(name__icontains=search_term).first()

        # 2. If bill is being submitted
        elif 'bill_submit' in request.POST:
            patient_id = request.POST.get("patient_id")
            patient = get_object_or_404(Patient, id=patient_id)

            bill = Bill.objects.create(
                patient=patient,
                date=timezone.now()
            )

            product_ids = request.POST.getlist("product[]")
            amounts = request.POST.getlist("amount[]")

            total = 0
            for i in range(len(product_ids)):
                product = get_object_or_404(Product, id=product_ids[i])
                amount = float(amounts[i]) if amounts[i] else 0
                total += amount

                BillItem.objects.create(
                    bill=bill,
                    product=product,
                    quantity=1,
                    amount=amount
                )

            bill.amount = total
            bill.save()

            return redirect('bills')

    return render(request, 'create_bills.html', {
        'products': products,
        'patient': patient,
        'searched': searched,
        'hospital': hospital,
    })


def view_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    patient = bill.patient
    products = Product.objects.all()
    items = BillItem.objects.filter(bill=bill)
    hospital = Hospital.objects.all()

    if request.method == "POST":
        # Delete old bill items
        bill.items.all().delete()

        # Get product IDs and amounts from POST data
        product_ids = request.POST.getlist("product[]")
        amounts = request.POST.getlist("amount[]")

        total = 0
        for i in range(len(product_ids)):
            if not product_ids[i]:
                continue  # Skip empty lines

            product = get_object_or_404(Product, id=product_ids[i])
            amount = float(amounts[i]) if amounts[i] else 0
            total += amount

            # Save each item
            BillItem.objects.create(
                bill=bill,
                product=product,
                quantity=1,
                amount=amount
            )

        # Update total amount (can also get from hidden input)
        total_from_form = request.POST.get("total_amount")
        if total_from_form:
            try:
                total = float(total_from_form)
            except ValueError:
                pass

        bill.amount = total
        bill.save()

        return redirect('bills')  # replace 'bills' with your actual URL name

    return render(request, 'view_bill.html', {
        'bill': bill,
        'patient': patient,
        'products': products,
        'items': items,
        'hospital': hospital,
    })
