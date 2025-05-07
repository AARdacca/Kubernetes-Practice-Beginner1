from django.contrib import admin
from django.urls import path

from .views import *

app_name = "auth"

urlpatterns = [
    path('login', login_view, name="login"),
    path('register', register_view, name="Register View"),
    path('logout', logout_view, name="Logout View"),
    path('user/', change_user_credintials, name="Change User Credintials View"),
    path('change_pass/', change_password, name="Change Password  View"),

    path('account/', account, name="account")
   
]
