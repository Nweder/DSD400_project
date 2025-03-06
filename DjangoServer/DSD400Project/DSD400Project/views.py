from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import SignUpForm
from .models import Reservation, Car

def homePage(request):
    cars = Car.objects.all()  # Fetch cars
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect(reverse('homePage'))
    else:
        return render(request, 'home.html',{'cars': cars})

def aboutPage(request):
    return render(request, 'about.html')

def registerPage(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username') # Authenticate and login
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect(reverse('homePage'))
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect(reverse('homePage'))

def reservePage(request):
    if request.user.is_authenticated:
        reservations = Reservation.objects.filter(userId=request.user)
        return render(request, 'reservation.html', {'reservations': reservations})
    else:
        return redirect(reverse('homePage'))

def deleteReservation(request, pk):
    if request.user.is_authenticated:
        reservation = Reservation.objects.get(reservationId=pk)
        reservation.carId.isAvailable = True
        reservation.carId.save()
        reservation.delete()
        return redirect(reverse('reservePage'))
    else:
        return redirect(reverse('homePage'))   
    
def bookPage(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            brand = request.GET.get('brand', '')
            car_type = request.GET.get('type', '')
            size = request.GET.get('size', '')
            transmission = request.GET.get('transmission', '')
            fuel_type = request.GET.get('fuelType', '')
            date_from = request.GET.get('dateFrom', '')
            date_to = request.GET.get('dateTo', '')

            cars = Car.objects.filter(isAvailable=True)

            if brand:
                cars = cars.filter(brand=brand)
            if car_type:
                cars = cars.filter(type=car_type)
            if size:
                cars = cars.filter(size=size)
            if transmission:
                cars = cars.filter(transmission=transmission)
            if fuel_type:
                cars = cars.filter(fuelType=fuel_type)
            if date_from and date_to:
                cars = cars.filter(booking_start__gte=date_from, booking_end__lte=date_to)

            return render(request, 'book.html', {'cars': cars})
    else:
        return redirect(reverse('homePage'))
    
def bookCar(request, pk):
    if request.user.is_authenticated:
        car = Car.objects.get(carId=pk)
        if car.isAvailable == True:
            reservation = Reservation(userId=request.user, carId=car)
            reservation.save()
            car.isAvailable = False
            car.save()
            return redirect(reverse('bookPage'))
        else:
            # Här borde vi lägga till ett meddelande att bilen inte är tillgänglig
            return redirect(reverse('bookPage'))