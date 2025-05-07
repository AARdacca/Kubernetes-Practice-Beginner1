from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import timedelta
from django.core.serializers import serialize
from lottery.models import Category
from .models import Slider
from order.models import Winner
import json

def home(request):

    catagories = Category.objects.all()
    three_days_after = timezone.now() + timedelta(days=3)
    lottery = Slider.objects.filter(is_active = True).order_by('-id')
    lottery_json = data = []

    for item in lottery:
        lottery_json.append({
            'id': item.competition.id,
            'name': item.name,
            'des' : item.description,
            'image': request.build_absolute_uri(item.image.url) if item.image else None,
            'mobile_image' : request.build_absolute_uri(item.mobile_image.url) if item.image else None
            
        })
    lottery_json = json.dumps(lottery_json)
    return render(request, 'index.html', context={'catagories':catagories,'lottery_json':lottery_json})
    



def winners_view(request):

    winners = Winner.objects.all().order_by('-id')
    return render(request, 'winners.html', context={'winners':winners})



def recent_tickets(request):

    return render(request, 'components/recent-tickets.html')

