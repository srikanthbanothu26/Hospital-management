from django.urls import path
from .views import patients, create_patient, edit_patient, bulk_delete_patients, patient_pdf_view, patient_pdf_download, \
    Bills, create_bill, delete_bill, view_bill, bulk_delete_bills

urlpatterns = [
    path('patients/', patients, name='patients'),
    path('create_patient/', create_patient, name='create_patient'),
    path('edit_patient/<int:patient_id>/', edit_patient, name='edit_patient'),
    path('patients/bulk_delete/', bulk_delete_patients, name='bulk_delete_patients'),
    path('patient/<int:patient_id>/pdf/preview/', patient_pdf_view, name='patient_pdf_preview'),
    path('patient/<int:patient_id>/pdf/download/', patient_pdf_download, name='patient_pdf_download'),
    path('bills/', Bills, name='bills'),
    path('create_bill/', create_bill, name='create_bill'),
    path('bills/delete/<int:bill_id>/', delete_bill, name='delete_bill'),
    path('view_bill/<int:bill_id>/', view_bill, name='view_bill'),
    path('bills/bulk_delete/', bulk_delete_bills, name='bulk_delete_bills'),

]
