# Här skapas object för databasen.
# Varje object är en klass som ärver från models.Model
# Varje klass representerar en tabell i databasen
# Varje attribut representerar en kolumn i tabellen
# Varje attribut är en instans av en klass som ärver från models.Field
# Varje instans av en Field-klass representerar en datatyp för en kolumn
# Varje instans av en Field-klass kan ha olika argument för att specificera beteende

from django.db import models
from django.core.exceptions import ValidationError

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

class Car(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    size = models.CharField(
        max_length=20, 
        choices=[("Small", "Small"), ("Medium", "Medium"), ("Large", "Large")]
    )
    fuel_type = models.CharField(
        max_length=20, 
        choices=[("Petrol", "Petrol"), ("Diesel", "Diesel"), ("Electric", "Electric")]
    )
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.size})"
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Koppling till Django-användaren
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    booking_from = models.DateField()
    booking_to = models.DateField()
    status = models.CharField(
        max_length=20, 
        choices=[("Pending", "Pending"), ("Confirmed", "Confirmed"), ("Cancelled", "Cancelled")], 
        default="Pending"
    )
    def clean(self):
        # Kontrollera om bilen är ledig under den valda perioden
        overlapping_bookings = Booking.objects.filter(
            car=self.car,
            booking_from__lt=self.booking_to,
            booking_to__gt=self.booking_from,
            status="Confirmed"
        ).exists()

        if overlapping_bookings:
            raise ValidationError("Denna bil är redan bokad under denna period.")


    def __str__(self):
        return f"Booking {self.id} - {self.user.username} - {self.car.brand} {self.car.model}"