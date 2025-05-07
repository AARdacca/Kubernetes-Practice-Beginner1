# runapscheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone

from order.models import Winner

from .models import Lottery


def draw(instance):
    print(f"draw for Competation : {instance.name}")
    ticket = instance.lotteryticket_set.all().order_by('?').first()
    if ticket:
        Winner.objects.create(user = ticket.user, lottery = instance, ticket=ticket)
        instance.has_perform_draw = True
        instance.save()
    



def check_date():
    print("Scanning All Lottery")
    lottery = Lottery.objects.filter(draw_in__lte=timezone.now(),has_perform_draw=False)

    for i in lottery:
        draw(i)

def update_something():
    check_date()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_something, 'interval', seconds=120)
    scheduler.start()