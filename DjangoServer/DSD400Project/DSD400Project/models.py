from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

class User():
    pass
    # Denna änvänds inte längre, utan vi ska använda Django's inbyggda User model istället
    # settings.AUTH_USER_MODEL som foreign key
    # Detta gör att länkar djangos User till våra models
    # https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project  

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
    startDate = models.DateField() # sätter datumet till dagens datum, används tills vi implementerar kalender
    endDate = models.DateField() # sätter datumet till dagens datum, används tills vi implementerar kalender



    # def clean(self):
    #     if Reservation.objects.filter(
    #         carId=self.carId,
    #         startDate__lt=self.endDate,
    #         endDate__gt=self.startDate,
    #     ).exists():
    #         raise ValidationError("Denna bil är redan bokad under denna period {startDate__lt} {endDate__gt} .")
