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
    carId = models.ForeignKey(Car, on_delete=models.CASCADE)
    userId = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()

    def clean(self):
        overlapping_bookings = Reservation.objects.filter(
            carId=self.carId,
            startDate__lt=self.endDate,
            endDate__gt=self.startDate,
        ).exists()

        if overlapping_bookings:
            raise ValidationError("Denna bil är redan bokad under denna period.")

    
