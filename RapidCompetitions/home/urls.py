from django.contrib import admin
from django.urls import include, path

from .views import *

urlpatterns = [
    path('', home, name="Homepage Rendering"),
    path('winners/', winners_view, name="winners"),

    path('recent-tickets/', recent_tickets, name="recent_tickets"),


]
