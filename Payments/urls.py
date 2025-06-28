from django.urls import path
from .views import create_payment, Payments

urlpatterns = [
    path('payments/', Payments, name='payments'),
    path('payments/create/<int:bill_id>/', create_payment, name='create_payment'),
]
