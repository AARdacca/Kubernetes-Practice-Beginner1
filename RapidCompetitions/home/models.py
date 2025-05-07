from django.db import models

from lottery.models import Lottery

class Slider(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True,blank=True)
    image = models.ImageField(upload_to='Slider/')
    mobile_image = models.ImageField(upload_to='SliderMobile/', null=True,blank=True)
    competition = models.ForeignKey(Lottery, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    def __str__(self) -> str:
        return self.name
    


