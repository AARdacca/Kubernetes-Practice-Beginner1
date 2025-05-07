from django.contrib import admin
from django.urls import include, path

from .views import *

urlpatterns = [
    path('', checkout_view, name="CheckOut View Page"),
    path('payment/<int:pk>/', payment_view, name="Payment View Page"),
    path('success/<int:pk>/', success_view, name="Payment Success View Page"),
    path('cancel/<int:pk>/', cancel_view, name="Payment Cancel View Page"),
    path('checkout/<int:pk>/',checkout_with_saved_data, name="Checkout With Saved Data")
]
