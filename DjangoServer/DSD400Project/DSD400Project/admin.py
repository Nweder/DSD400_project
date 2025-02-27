from django.contrib import admin
from .models import User, Cars, Reservation

admin.site.register(User)
admin.site.register(Cars)
admin.site.register(Reservation)