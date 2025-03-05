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
        reservation.delete()
        return redirect(reverse('reservePage'))
    else:
        return redirect(reverse('homePage'))   