from django.db import models

from authentication.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name
    



class Lottery(models.Model):
    class Meta:
        verbose_name = "Competition"
        verbose_name_plural = "Competitions"

    CASH_ALTERNATIVE_STATUS = [
        ("YES", "Yes"),
        ("NO", "NO"),

    ]
    DRAW_BY = [
        ("MANUAL", "Manual"),
        ("AUTO", "Auto"),
    ]
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="Competition/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True,blank=True)
    have_any_cash_alternative = models.CharField(max_length=80, choices=CASH_ALTERNATIVE_STATUS, default="NO")
    cash_alternative = models.IntegerField(null=True,blank=True)
    draw_in = models.DateTimeField()
    price = models.DecimalField(decimal_places = 2, max_digits=10)
    total_available_ticket = models.IntegerField()
    total_sold = models.IntegerField(default=0)
    max_entries_per_user = models.IntegerField(default=1)
    suggested_ticket_quantity = models.IntegerField(default=1)
    draw_by = models.CharField(max_length=20, choices=DRAW_BY, default="AUTO")
    has_perform_draw = models.BooleanField(default=False)
    price_details = models.TextField(null=True,blank=True)
    def __str__(self) -> str:
        return self.name
    
class LotteryImage(models.Model):
    class Meta:
        verbose_name = "CompetitionImage"
        verbose_name_plural = "CompetitionImages"
        
    lottery = models.ForeignKey(Lottery,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Lottery/")

    def __str__(self):
        return self.lottery.name


