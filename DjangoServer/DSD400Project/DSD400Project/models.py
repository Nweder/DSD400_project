# Här skapas object för databasen.
# Varje object är en klass som ärver från models.Model
# Varje klass representerar en tabell i databasen
# Varje attribut representerar en kolumn i tabellen
# Varje attribut är en instans av en klass som ärver från models.Field
# Varje instans av en Field-klass representerar en datatyp för en kolumn
# Varje instans av en Field-klass kan ha olika argument för att specificera beteende

from django.db import models

# Create your models here.
class User (models.Model):
    # Argumentet max_length specificerar maxlängden för en sträng i kolumnen
    userId = models.IntegerField(max_length=50, primary_key=True)
    email = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50) 
    password = models.CharField(max_length=50)
    models.PhoneNumberField(("phone number"), max_length=50, unique=True)

class Cars (models.Model):
    carId = models.IntegerField(max_length=50, primary_key=True)
    brand = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    isReserved = models.BooleanField()

    # Detta syns bara av admin, så man kan få en överblick över vilka bilar som är reserverade
    reservedByUserId = models.ForeignKey(User, on_delete=models.CASCADE)

class Reservation(models.Model):
    reservationId = models.IntegerField(max_length=50, primary_key=True)
    carId = models.ForeignKey(Cars, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    
    startDate = models.DateField()
    endDate = models.DateField()