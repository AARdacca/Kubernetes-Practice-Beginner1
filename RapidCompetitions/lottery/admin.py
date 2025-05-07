from django.contrib import admin

from .models import Category, Lottery, LotteryImage


class LotteryImageInline(admin.TabularInline):
    model = LotteryImage
    extra = 1


# Custom admin class for the Course model
class LotteryAdmin(admin.ModelAdmin):
    inlines = [LotteryImageInline]
    list_display = ('name', 'draw_in', 'price', 'total_sold','total_remaining','id','category')

    def total_remaining(self,obj):
        return obj.total_available_ticket - obj.total_sold



admin.site.register(Category)
admin.site.register(Lottery, LotteryAdmin)

# Register your models here.
