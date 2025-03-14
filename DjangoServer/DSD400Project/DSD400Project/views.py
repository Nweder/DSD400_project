from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import SignUpForm
from .models import Reservation, Car
from datetime import datetime
from django.contrib import messages
from django.db import transaction


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
        with transaction.atomic():
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
        if 'dateFrom' not in request.session or 'dateTo' not in request.session:
            messages.error(request, 'Please select a date range before choosing a car.')
            return redirect(reverse('selectDatesPage')) 

        date_from = request.session.get('dateFrom', '')
        date_to = request.session.get('dateTo', '')

        brand = request.GET.get('brand', '')
        car_type = request.GET.get('type', '')
        size = request.GET.get('size', '')
        transmission = request.GET.get('transmission', '')
        fuel_type = request.GET.get('fuelType', '')

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

        return render(request, 'book.html', {'cars': cars, 'dateFrom': date_from, 'dateTo': date_to})
    else:
        return redirect(reverse('homePage'))
    

def bookCar(request, pk):
    if request.user.is_authenticated:
        
        car = Car.objects.filter(carId=pk).first() 
        date_from = request.session.get('dateFrom', None)
        date_to = request.session.get('dateTo', None)

        if not date_from or not date_to:
            messages.error(request, "You must select a date before booking a car.")
            return redirect(reverse('selectDatesPage'))
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Please try again.")
            return redirect(reverse('selectDatesPage'))
        with transaction.atomic():
            reservation = Reservation(userId=request.user, carId=car, startDate=date_from, endDate=date_to)
            reservation.save()
            car.isAvailable = False
            car.save()
            
            messages.success(request, "Car has been booked successfully!")
            return redirect(reverse('bookPage'))
    else:
        messages.error(request, "You need to be logged in to book a car.")
        return redirect(reverse('homePage'))
    

def selectDatesPage(request):
    return render(request, 'select_dates.html')

def setBookingDates(request):
    if request.method == 'POST':
        date_from = request.POST.get('dateFrom')
        date_to = request.POST.get('dateTo')

        request.session['dateFrom'] = date_from
        request.session['dateTo'] = date_to
        request.session.modified = True 

        return redirect(reverse("bookPage"))  

    return render(request, "select_dates.html")
