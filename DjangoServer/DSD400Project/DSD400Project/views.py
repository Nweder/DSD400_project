from django.shortcuts import render

def homePage(request):
    return render(request, 'home.html')

def aboutPage(request):
    return render(request, 'about.html')

def userPage(request):
    return render(request, 'user.html')
    