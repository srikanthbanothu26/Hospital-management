from django.urls import path
from .views import index, create_doctor, update_doctor, create_department, update_department, medicines, \
    create_medicine, update_medicine, delete_medicine, user_info_view, get_states, create_profession, profession_list, \
    profession_detail, departments_list, delete_department, bulk_delete_departments, specialists_list, \
    bulk_delete_doctors, delete_doctor, delete_profession

urlpatterns = [
    path('', index, name='index'),
    path('create_doctor/', create_doctor, name='create_doctor'),
    path('doctors/<int:doctor_id>/edit/', update_doctor, name='update_doctor'),
    path('specialists/', specialists_list, name='specialists_list'),
    path('delete_doctor/<int:doctor_id>/', delete_doctor, name='delete_doctor'),
    path('specialists/bulk-delete/', bulk_delete_doctors, name='bulk_delete_doctors'),
    path('departments/create/', create_department, name='create_department'),
    path('departments/<int:department_id>/edit/', update_department, name='update_department'),
    path('medicines/', medicines, name='medicines'),
    path('medicines/create/', create_medicine, name='create_medicine'),
    path('medicines/<int:product_id>/edit/', update_medicine, name='update_medicine'),
    path('medicines/<int:product_id>/delete/', delete_medicine, name='delete_medicine'),
    path('user_info/<int:user_id>/', user_info_view, name='user_info'),
    path('get-states/', get_states, name='get_states'),
    path('profession/<int:profession_id>/', profession_detail, name='profession_detail'),
    path('profession/create/', create_profession, name='create_profession'),
    path('professions/', profession_list, name='professions'),
    path('profession/<int:profession_id>/delete/', delete_profession, name='delete_profession'),
    path('departments_list/', departments_list, name='departments_list'),
    path('departments/<int:department_id>/delete/', delete_department, name='delete_department'),
    path('departments/bulk-delete/', bulk_delete_departments, name='bulk_delete_departments'),
]
