from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    userId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, default='username')
    password = models.CharField(max_length=50, default='password')
    email = models.EmailField(default='email')
    

    def __str__(self):
        return self.username 

class Car(models.Model):
    carId = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=50, default='brand') #märke (volvo, bmw, etc)
    type = models.CharField(max_length=50,default='type')  #typ (suv, sedan, kombi, etc)
    size = models.CharField(max_length=50, default='size') #storlek (liten, mellan, stor)
    transmission = models.CharField(max_length=50, default='trans') #växellåda - automat eller manuell
    fuelType = models.CharField(max_length=50, default="fuel") #bränsle - bensin, diesel, el, etc

    # Följande 2 attribut är tror jag ska ligga på reservation istället, vi kollar upp det sen    
    isReserved = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

class Reservation(models.Model):
    reservationId = models.AutoField(primary_key=True)
    carId = models.ForeignKey(Car.carId, on_delete=models.CASCADE)
    userId = models.ForeignKey(User.userId,on_delete=models.CASCADE)

    startDate = models.DateField()
    endDate = models.DateField()

    def clean(self):
        if Reservation.objects.filter(
            carId=self.carId,
            startDate__lt=self.endDate,
            endDate__gt=self.startDate,
        ).exists():
            raise ValidationError("Denna bil är redan bokad under denna period {startDate__lt} {endDate__gt} .")
