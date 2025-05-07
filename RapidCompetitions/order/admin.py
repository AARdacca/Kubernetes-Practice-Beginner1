from django.contrib import admin

from .models import *

# Register your models here.

class OrderItemTabularInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderModelAdmin(admin.ModelAdmin):
    inlines = [OrderItemTabularInline]


admin.site.register(Order,OrderModelAdmin)
admin.site.register(Winner)
admin.site.register(LotteryTicket)