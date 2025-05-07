from django.db import models

from authentication.models import User
from lottery.models import Lottery


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    date_of_birth = models.DateField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, null=True,blank=True)
    town = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField()
    sign_me_up = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)
    total_price = models.DecimalField(decimal_places = 2, max_digits=10, null=True,blank=True)

    def __str__(self) -> str:
        return f'Order Id : {self.id} User Email: {self.email}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Lottery,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f'OrderId : {self.order.id} ItemId : {self.id}'
    

class LotteryTicket(models.Model):
    class Meta:
        verbose_name = "Competition Ticket"
        verbose_name_plural = "Competition Tickets"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lottery = models.ForeignKey(Lottery,on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Winner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE)
    ticket = models.ForeignKey(LotteryTicket, on_delete=models.CASCADE, null=True, blank=True)
    winner_photo = models.ImageField(upload_to='Winners/', null=True,blank=True)