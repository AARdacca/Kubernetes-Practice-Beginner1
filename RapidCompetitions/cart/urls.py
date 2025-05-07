from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [
    path('', cart_view, name="Cart View Page"),

]
