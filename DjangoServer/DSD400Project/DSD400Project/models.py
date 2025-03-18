from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


class Car(models.Model):
    carId = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=50, 
        choices=[('Volvo', 'Volvo'), ('BMW', 'BMW'), ('Audi', 'Audi')]
    ) # märket (volvo, bmw, etc)
    type = models.CharField(max_length=50, 
        choices=[('SUV', 'SUV'), ('Sedan', 'Sedan'), ('Combi', 'Combi')]
    ) # typ (suv, sedan, kombi, etc)
    size = models.CharField(max_length=50, 
        choices=[('small', 'Small'), ('medium', 'Medium'), ('big', 'Big')]
    ) # storlek (liten, mellan, stor)
    transmission = models.CharField(max_length=50, 
        choices=[('automatic', 'Automatic'), ('manual', 'Manual')]
    ) # växellåda - automat eller manuell
    fuelType = models.CharField(max_length=50, 
        choices=[('gas', 'Gas'), ('electric', 'Electric')]
    ) # bränsle - bensin, diesel, el, etc
    isAvailable = models.BooleanField(default=True)


class Reservation(models.Model):
    reservationId = models.AutoField(primary_key=True)
    carId = models.ForeignKey(Car, on_delete=models.CASCADE)
    userId = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    startDate = models.DateField() 
    endDate = models.DateField() 