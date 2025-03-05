from django.contrib import admin
from .models import User, Car, Reservation

admin.site.register(User)
admin.site.register(Car)
admin.site.register(Reservation)
