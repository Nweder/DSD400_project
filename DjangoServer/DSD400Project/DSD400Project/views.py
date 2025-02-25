from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

def homePage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('homePage'))
        else:
            return redirect(reverse('homePage'))
    else:
        return render(request, 'home.html')

def aboutPage(request):
    return render(request, 'about.html')

def registerPage(request):
    pass