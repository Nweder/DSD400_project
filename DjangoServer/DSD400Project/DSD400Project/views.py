from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import SignUpForm
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from .models import Reservation, Cars, User
import json
from django.http import JsonResponse
from django.contrib.auth.models import User


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User  
from .models import Cars, Reservation
import json


def homePage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        cars = Cars.objects.all()  # Fetch cars
        reservations = Reservation.objects.filter(userId=request.user)  # Fetch reservations for the logged-in user
        context = {
            'cars': cars,
            'reservations': reservations
        }
        return redirect(reverse('homePage'))
    else:
        return render(request, 'home.html')

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

def create_reservation(request): ##New Function to create oweer reservation
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        user_id = request.POST.get('user_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        try: # Create a new reservation
            car = Cars.objects.get(id=car_id)
            user = User.objects.get(id=user_id)
            reservation = Reservation(carId=car, userId=user, startDate=start_date, endDate=end_date)
            reservation.clean()  # Check for overlapping reservations
            reservation.save()

            return HttpResponse("Reservation created successfully!")

        except ValidationError as e:
            return HttpResponse(f"Error: {e.message}")

    return render(request, 'reservation_form.html')

def signup_user(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

        else:
            username = request.POST['username']
            password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'User already exists.'}, status=400)
        
        user = User.objects.create_user(username=username, password=password)

        return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})

    return render(request, 'signup.html') 

def get_cars(request):
    brand = request.GET.get('brand', '')
    size = request.GET.get('size', '')
    fuel_type = request.GET.get('fuelType', '')

    cars = Cars.objects.filter(
        brand__icontains=brand,
        size__icontains=size,
        fuelType__icontains=fuel_type
    )

    car_data = [{"id": car.id, "brand": car.brand, "size": car.size, "fuelType": car.fuelType} for car in cars]

    return JsonResponse(car_data, safe=False)


def add_booking(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        car_id = data.get('car_id')
        date_from = data.get('date_from')
        date_to = data.get('date_to')

        try:
            user = User.objects.get(id=user_id)
            car = Cars.objects.get(id=car_id)
        except (User.DoesNotExist, Cars.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Invalid user or car ID.'}, status=400)

        overlapping_bookings = Reservation.objects.filter(
            carId=car,
            startDate__lt=date_to,
            endDate__gt=date_from,
        ).exists()

        if overlapping_bookings:
            return JsonResponse({'status': 'error', 'message': 'The car is already booked for the selected dates.'}, status=400)

        reservation = Reservation(userId=user, carId=car, startDate=date_from, endDate=date_to)
        reservation.save()

        return JsonResponse({'status': 'success', 'message': 'Booking confirmed!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Logged in successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials.'}, status=400)
    return render(request, 'login.html')