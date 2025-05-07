from datetime import timedelta

from django import template
from django.utils import timezone

from authentication.models import Checkout
from lottery.models import Category

register = template.Library()


@register.filter
def is_category_empty(value):
    if value.lottery_set.filter(draw_in__gte=timezone.now()).exists():
        return False
    else:
        return True
    

@register.filter
def give_me_ending_soon_lottery_list(instance):
    three_days_after = timezone.now() + timedelta(days=3)
    return instance.lottery_set.filter(draw_in__gte=timezone.now(), draw_in__lte = three_days_after).order_by('draw_in')

@register.filter
def give_me_all_lottery_of_a_category(instance):
    return instance.lottery_set.filter(draw_in__gte=timezone.now()).order_by('draw_in')
    
@register.filter
def perform_subtract(value1,value2):
    return value1-value2

@register.filter
def perform_percentage(value, total):
    return int((100*value)/total)

@register.filter
def get_all_category(value):
    return Category.objects.all()

@register.filter
def get_chckout_instances(value):
    return Checkout.objects.filter(user=value)

@register.filter
def is_any_saved_checkout(value):
    return Checkout.objects.filter(user=value).exists()


@register.filter
def is_lottery_image_set_empty(value):
    return value.exists()