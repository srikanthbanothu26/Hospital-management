from django.shortcuts import render, get_object_or_404, redirect
from Home.models import *
from decimal import Decimal
from datetime import datetime
from django.db.models import Sum


def generate_payment_ref():
    year = datetime.now().year
    last_payment = Payment.objects.filter(ref__startswith=f"PAY/{year}/").order_by('-id').first()

    if last_payment and last_payment.ref:
        try:
            last_seq = int(last_payment.ref.split('/')[-1])
        except:
            last_seq = 0
    else:
        last_seq = 0

    new_seq = str(last_seq + 1).zfill(5)
    return f"PAY/{year}/{new_seq}"


def create_payment(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    if bill.status != 'draft':
        return redirect('payments')

    patient = bill.patient
    payment_methods = PaymentMethod.objects.all()
    upi_methods = UpiPayments.objects.all()

    if request.method == 'POST':
        method_name = request.POST.get('payment_method')
        amount = request.POST.get('amount') or bill.amount
        amount = Decimal(amount)

        payment_method = PaymentMethod.objects.get(name=method_name.lower())
        ref = generate_payment_ref()

        if method_name == 'cash':
            # Using fixed DebitAccount ID=1 and CreditAccount ID=2
            debit_account = get_object_or_404(DebitAccount, id=2)
            credit_account = get_object_or_404(CreditAccount, id=1)

            Payment.objects.create(
                ref=ref,
                payment_method=payment_method,
                patient=patient,
                bill=bill,
                debit=amount,
                credit=0,
                balance=0,
                status='paid',
                debit_account=debit_account,
                credit_account=credit_account,
            )

            bill.status = 'done'
            bill.save()

        elif method_name == 'bank':
            # Optionally collect entered bank details
            acc_name = request.POST.get('debit_account_name')
            ifsc = request.POST.get('debit_ifsc_code')

            debit_account = get_object_or_404(DebitAccount, id=3)
            credit_account = get_object_or_404(CreditAccount, id=2)

            Payment.objects.create(
                ref=ref,
                payment_method=payment_method,
                patient=patient,
                bill=bill,
                debit=amount,
                credit=amount,
                balance=0,
                status='paid',
                debit_account=debit_account,
                credit_account=credit_account,
            )

            bill.status = 'done'
            bill.save()

        return redirect('payments')

    context = {
        'bill': bill,
        'patient': patient,
        'payment_methods': payment_methods,
        'upi_methods': upi_methods,
    }

    return render(request, "create_payments.html", context)


def Payments(request):
    hospital = Hospital.objects.all()
    payments = Payment.objects.all()
    total_sum = payments.aggregate(Sum('debit'))['debit__sum'] or 0
    return render(request, "payments.html", {
        'payments': payments,
        'hospital': hospital,
        'total_sum': total_sum,
    })
