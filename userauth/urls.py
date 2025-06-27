from django.urls import path
from .views import register, login, logout, update_password

urlpatterns = [
    path("login/", login, name="user_login"),
    path("register/", register, name="user_register"),
    path("logout/", logout, name="user_logout"),
    path("update_password/", update_password, name="password_reset"),
]
