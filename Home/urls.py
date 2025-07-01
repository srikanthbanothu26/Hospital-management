from django.urls import path
from .views import index, create_doctor, update_doctor, create_department, update_department, medicines, \
    create_medicine, update_medicine, delete_medicine, user_info_view, get_states

urlpatterns = [
    path('', index, name='index'),
    path('create_doctor/', create_doctor, name='create_doctor'),
    path('doctors/<int:doctor_id>/edit/', update_doctor, name='update_doctor'),
    path('departments/create/', create_department, name='create_department'),
    path('departments/<int:department_id>/edit/', update_department, name='update_department'),
    path('medicines/', medicines, name='medicines'),
    path('medicines/create/', create_medicine, name='create_medicine'),
    path('medicines/<int:product_id>/edit/', update_medicine, name='update_medicine'),
    path('medicines/<int:product_id>/delete/', delete_medicine, name='delete_medicine'),
    path('user_info/<int:user_id>/', user_info_view, name='user_info'),
    path('get-states/', get_states, name='get_states'),
]
